"""Main logic of the preprocessor articulating the different core steps of
transforming a single dataset into ML-Ready data.
"""

from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass
import time
import tempfile
import random
import gc

# Dependencies
import pandas as pd
import numpy as np

# Private Dependencies
from evoml_api_models import PreprocessedMetadata, MlTask

# Module
from evoml_preprocessor.preprocess.models import PreprocessConfig, ColumnInfo
from evoml_preprocessor.preprocess.models.report import PreprocessingReport
from evoml_preprocessor_internal.preprocess.preprocessor import EvomlDataPreprocessor
from evoml_preprocessor.splitting import SplitData, split
from evoml_preprocessor.utils.log import log_memory
from evoml_preprocessor_internal.utils.io_structure import OutputFlags
from evoml_preprocessor.utils.sort import sort_datasets_index

# ─────────────────────────── input/output classes ─────────────────────────── #


@dataclass
class PreprocessOutputs:
    """Contains auxiliary outputs of the preprocessor"""

    # Preprocessed DataFrames
    train: pd.DataFrame
    test: Optional[pd.DataFrame]  # when using `nosplit`
    metadata: PreprocessedMetadata

    # Split indices (to know how the data hads been split)
    train_idx: Optional[pd.Index]  # Index of the train data
    test_idx: Optional[pd.Index]  # Index of the test data
    train_drop_idx: Optional[pd.Index]  # Dropped indices from original train
    test_drop_idx: Optional[pd.Index]  # Dropped indices from original test

    # @TODO: temporary, waiting for BW + Thanos integration
    split_data: Optional[SplitData]

    # Appendix code, given as a temporary directory (see `tempfile.mkdtemp`),
    # you will need to delete it
    appendix_dir: Optional[Path]

    # (version, extras) of the 'evoml_preprocessor' library
    library_version: Tuple[str, List[str]]

    # Report giving details on decisions made
    report: PreprocessingReport


def preprocess(
    config: PreprocessConfig,
    types: List[ColumnInfo],
    dataset: pd.DataFrame,
    dataset_test: Optional[pd.DataFrame] = None,
    output_flags: OutputFlags = OutputFlags(),
) -> PreprocessOutputs:
    """This is the main entry point from evoml-preprocess

    Preprocesses the given dataset, using the types/anomalies detected

    Args:
        config (PreprocessConfig):
            Initial configuration of the file
        types (List[ColumnInfo]):
            Types and anomalies detected during the earlier steps
        dataset (pd.DataFrame):
            Pandas DataFrame containing the original data to process
        dataset_test (pd.DataFrame, optional):
            separate test file specified by the user. Required if splitting method
            is pre-split.
        output_paths (Outputs, optional):
            path to the output

    Returns:
        (preprocessed_train, preprocessed_test, report):
            Preprocessed train and test dataframes, and the preprocessing report
    """
    preprocess_start_time = time.time()  # in seconds

    # Set a deterministic seed for random number generation
    random.seed(config.seed)
    np.random.seed(config.seed)

    # Convert the list of column info to a map {name → info}
    info_map = {info.name: info for info in types}

    log_memory("Data loaded from disk", dataset)

    # -------------------------- dataframe sorting --------------------------- #
    # Sorts the dataframe by index for timeseries tasks
    if config.isTimeseries and config.indexColumn is not None:
        # Sort with respect to indexColumn in case that dataset is not sorted
        dataset, dataset_test = sort_datasets_index(dataset, config.indexColumn, info_map, dataset_test)
        log_memory("Original data sorted by index", dataset)

    # --------------------------- train/test split --------------------------- #
    split_data = split(dataset, config, info_map, dataset_test)
    split_train_idx = split_data.train.index.copy()
    split_test_idx = split_data.test.index.copy()

    gc.collect()

    log_memory("Split train data", split_data.train)
    log_memory("Split test data", split_data.test)

    # ------------------------ run the preprocessing ------------------------- #
    processor = EvomlDataPreprocessor.from_config(config, info_map)
    preprocessed_train = processor.fit_transform(split_data.train, config.labelColumn)
    preprocessed_test = processor.transform(split_data.test, True)

    log_memory("Preprocessed test data", preprocessed_test)

    # ------------------- train/test/dropped original data ------------------- #
    train_idx, test_idx = None, None
    dropped_train_idx, dropped_test_idx = None, None
    if output_flags.original_split:
        train_idx = preprocessed_train.index
        dropped_train_idx = split_train_idx.difference(train_idx)
        if preprocessed_test is not None:
            test_idx = preprocessed_test.index
            dropped_test_idx = split_test_idx.difference(test_idx)

    # ------------------------------ reporting ------------------------------- #
    # Get preprocessor logs
    preprocess_end_time = time.time()
    processor.report_builder.totalPreprocessingTime = preprocess_end_time - preprocess_start_time

    report = processor.report_builder.build()

    # ------------------------- appendix generation -------------------------- #
    directory: Optional[Path] = None
    if output_flags.appendix:
        directory = Path(tempfile.mkdtemp())

        from evoml_preprocessor.utils.codegen import Appendix

        appendix = Appendix(directory)
        appendix.mkdir()
        processor.remove_nonpickled_attributes()
        processor.save_joblib(appendix.joblib)
        processor.save_requirements(appendix.requirements)

    return PreprocessOutputs(
        train=preprocessed_train,
        test=preprocessed_test,
        metadata=PreprocessedMetadata.parse_obj(processor.metadata),
        library_version=processor.get_requirements_extras(),
        appendix_dir=directory,
        train_idx=train_idx,
        test_idx=test_idx,
        train_drop_idx=dropped_train_idx,
        test_drop_idx=dropped_test_idx,
        report=report,
        # @TODO: temporary
        split_data=split_data,
    )
