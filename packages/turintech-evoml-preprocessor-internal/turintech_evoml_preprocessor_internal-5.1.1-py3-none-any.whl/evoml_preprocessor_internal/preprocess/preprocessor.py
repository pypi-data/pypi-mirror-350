# encoding: utf-8
"""
Single module gathering all the preprocessing logic. By design, this module
is meant to be standalone (this python file can be extracted from its context
and work).

It contains one main class, :class:`DataPreprocessor`, providing the public
interface for users as well as the top-level logic, and several classes
subclassing :class:`Transformer` providing the specific logic of preprocessing
different types of data.
"""
import gc

# ───────────────────────────────── imports ────────────────────────────────── #
# Standard Library
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Dependencies
import joblib
import pandas as pd
from evoml_api_models import MlTask

# Module
from evoml_preprocessor import _py_version
from evoml_preprocessor.preprocess.models import Filter, ReasonDropped
from evoml_preprocessor.preprocess.preprocessor import DataPreprocessor
from evoml_preprocessor.utils.anomaly_detection import get_rows_with_duplicate_index
from evoml_preprocessor.utils.conf.conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────── #
# Logger
logger = logging.getLogger("preprocessor")
# Alias to avoid very long constants
CONF = conf_mgr.preprocess_conf
# ──────────────────────────────────────────────────────────────────────────── #


class EvomlDataPreprocessor(DataPreprocessor):
    def fit_transform(self, data: pd.DataFrame, label_name: Optional[str] = None) -> pd.DataFrame:
        """Fits the preprocessor for a specific dataset, then transforms it

        This method fits the preprocessor to a dataset, then transforms that
        dataset. The output is a transformed dataset as a pandas dataframe.

        If you provide a label_name different than the one in the config file,
        the config will be updated. In that case, you might want to provide a
        path to save the updated config.json.

        You can also provide a path to save the fitted preprocessor object to
        the file-system (see optional arguments).

        NOTE: This function directly modifies the input dataframe.

        Args:
            data (pd.DataFrame):
                Dataset as a pandas dataframe, corresponding to the config.json
                and types.json provided to this object at instantiation.
            label_name (str, optional):
                Name of the column to use as labels (the column we want to
                predict). By default, uses the value provided in the
                config.json.
        Returns:
            pd.DataFrame:
                Transformed dataset as a pandas dataframe.
        """
        # -------------------------- safety checks --------------------------- #
        # Label name (2 sources: argument & self.config)
        self.config = self.config.copy(update={"label_column": label_name or self.config.label_column})
        if self.config.label_column not in data.columns:
            raise ValueError(f"Given label ({label_name}) does not exist in dataset {list(data.columns)}.")

        # Index
        if self.config.index_column and self.config.index_column not in data.columns:
            raise ValueError(
                f"Given index ({self.config.index_column}) does not exist in dataset {list(data.columns)}."
            )
        if self.config.index_column == self.config.label_column:
            raise ValueError(f"Target column {self.config.label_column} cannot be the index.")

        # ensure we have a valid index name
        if data.index.name is None:
            data.index.name = self.fitted_config.row_index_name
        else:
            self.fitted_config = self.fitted_config.copy(update={"row_index_name": data.index.name})

        # Consistency between the data and the column type info
        assert set(self.config.info_map.keys()) == set(data.columns)

        # ------------------------ setting attributes ------------------------ #
        self.fitted_config = self.fitted_config.copy(update={"original_columns": list(data.columns)})

        # ------------------------ drop anomaly rows ------------------------- #
        data, n_missing_rows = self._drop_anomaly_rows(data, self.config.label_column)
        self.report_builder.multiColumnStatistics.droppedRows = n_missing_rows

        # ---------------- processing the index column first ----------------- #
        encoded_to_original_map = {}  # initialize map for encoded names to original names

        # where self.config.index_column is the name of the index column found in the config file
        # Note: index_col represents the values of self.config.index_column
        if self.config.index_column:
            # index column provided in the config
            duplicates = get_rows_with_duplicate_index(data, self.config.index_column)
            if duplicates:
                data.drop(duplicates, inplace=True)
            index_info = self.config.info_map[self.config.index_column]
            index_col = data[self.config.index_column]
        else:
            # no index column provided in the config
            index_info = None
            index_col = None

        # generates an index column if needed, otherwise None is returned
        index_col = self.index_handler.fit_transform(
            index_info=index_info, index_col=index_col, index_size=data.shape[0]
        )
        # update report if needed
        if self.index_handler.feature_report is not None:
            self.report_builder.singleColumnStatistics += [self.index_handler.feature_report]

        # -------------------- create and index encoded dataset --------------------- #
        data_encoded = pd.DataFrame(index=data.index)

        # an index column was generated by the index handler
        if index_col is not None:
            # reindex the index column in case we created a new index
            index_col.index = data_encoded.index

            # if index column was not provided in the config but generated by index handler
            # update the index column name
            if self.config.index_column is None:
                # the case where we expected an index column but none was found, so we created a new one
                self.config.index_column = str(index_col.name)
            else:
                # if self.config.index_column is not None and index_col is not None then update the map
                encoded_to_original_map[index_col.name] = self.config.index_column

            # add index column to encoded data
            data_encoded = pd.concat([data_encoded, index_col], axis=1)
            # add encoded index to data - needed for some feature handlers
            data[index_col.name] = index_col

            #  set index names in handlers
            self.data_preparation_handler.index_name = str(self.config.index_column)
            self.feature_handler.index_name = self.config.index_column
        else:
            # no index column was generated by the index handler
            self.config.index_column = None

        # ---------------- processing the label column ----------------------- #

        logger.info(" Preprocess Train Set ".center(60, "-"))

        logger.info(" Label Column Transformation ".center(60, "-"))

        # Find the type information about the label column
        label_info = self.config.info_map[self.config.label_column]

        # Process the label column using a ml_task specific label handler
        label_handler = self.label_handler

        # Set index in label series for label_handler - needed for time series
        data_label = data[self.config.label_column]
        if index_col is not None:
            data_label.index = pd.Index(index_col, name=self.fitted_config.row_index_name)

        encoded_label, extra_label_features = label_handler.fit_transform(data_label)

        # Set index of encoded_label and extra_label_features to data.index
        encoded_label.index = data.index

        # Add encoded label column to data
        data[self.config.label_column] = encoded_label

        # get map from encoded label features to original names
        encoded_to_original_map.update(self.label_handler.encoded_to_original_map)

        logger.info(f"→ name: {label_info.name}")
        logger.info(f"→ type: {label_info.detectedType.value}")
        logger.info(f"→ encoder strategy: {label_handler.encoder_slug}")
        logger.info("→ label encoding successful")

        # Report label_column transformation
        self.report_builder.singleColumnStatistics += [label_handler.feature_report]

        # -------------------- Add encoded features using Feature Handler ---- #
        logger.info(" Column(s) Transformation ".center(60, "-"))
        data_encoded_trans = self.feature_handler.fit_transform(data, encoded_label)
        # join using inner method - needed as some transformers reduce number of rows
        data_encoded = data_encoded.join(data_encoded_trans, how="inner")

        # update report with singleColumnStatistics generated using feature_handler
        self.report_builder.singleColumnStatistics.extend(self.feature_handler.reports)

        # get map from encoded features to original names
        encoded_to_original_map.update(self.feature_handler.encoded_to_original_map)

        # Add extra label features
        if extra_label_features is not None:
            # Set index of extra label features
            extra_label_features.index = data.index[-extra_label_features.shape[0] :]
            data_encoded = data_encoded.join(extra_label_features, how="inner")

        # save memory by removing this temporary object before feature selection
        del data_encoded_trans
        del data
        gc.collect()

        # report number of columns generated after processing dataset with feature_handler
        self.report_builder.multiColumnStatistics.columnCountAfterFeatureHandler = len(data_encoded.columns)
        self.report_builder.multiColumnStatistics.encodedToOriginalMapping = encoded_to_original_map

        # ------------------------ Feature Selection ------------------------- #
        # update required columns for fs using encoded_to_original_map
        required_features: List[int] = [
            column.columnIndex
            for options in self.config.transformation_options
            for column in options.featureOverrides
            if column.filter == Filter.KEEP
        ]
        map_indexes_to_names: Dict[int, str] = {
            self.config.info_map[name].columnIndex: name for name in self.config.info_map.keys()
        }
        required_feature_names = [map_indexes_to_names[index] for index in required_features]
        required_encoded_features = [
            encoded_name
            for encoded_name, original_name in encoded_to_original_map.items()
            if original_name in required_feature_names
        ]

        if self.config.is_time_series:
            required_encoded_features.append(self.config.index_column)

        self.fs_handler.set_required_encoded_columns(required_encoded_features)
        data_encoded, selection_scores = self.fs_handler.fit_transform_report(data_encoded, encoded_label)

        if self.fs_handler.report is not None:
            self.report_builder.multiColumnStatistics.featureSelectionReport = self.fs_handler.report

        fs_removed_columns = self.fs_handler.removed_cols
        if len(fs_removed_columns) > 0:
            reports = self.report_builder.singleColumnStatistics

            # bin features removed by original name as feature report is grouped by original features
            reverse_map: Dict[str, List[str]] = {}
            for removed in fs_removed_columns:
                original_name = encoded_to_original_map[removed]

                if original_name in reverse_map:
                    reverse_map[original_name].append(removed)
                else:
                    reverse_map.update({original_name: [removed]})

            # update report to accurately represent columns dropped in feature selection
            for removed in reverse_map.keys():
                feature_report = next((x for x in reports if x.column_name == removed), None)

                if feature_report is not None:
                    items = reverse_map[removed]
                    transformation_block = feature_report.transformation_block

                    for block in transformation_block:
                        col_names = set(block.column_names)

                        # find subset of items removed from this block
                        removed_cols = col_names.intersection(items)
                        remaining_cols = col_names - removed_cols

                        block.column_names = list(remaining_cols)
                        block.column_dropped = list(removed_cols)

                        if removed_cols:
                            block.reason_dropped = ReasonDropped.FEATURE_SELECTOR
                else:
                    logger.error(f"column {removed} not found in feature report")

        # save the original features that are kept
        for encoded_column in data_encoded.columns:
            name: Optional[str] = encoded_to_original_map.get(encoded_column, None)
            if (
                name is not None
                and name not in self.fitted_config.required_columns
                and name != self.config.label_column
            ):
                required_columns = self.fitted_config.required_columns + [name]
                self.fitted_config = self.fitted_config.copy(update={"required_columns": required_columns})

        # ------------------------ Feature Generation ------------------------ #
        data_encoded = self.fg_handler.fit_transform_report(data_encoded, encoded_label, selection_scores)
        if self.fg_handler.report is not None:
            self.report_builder.multiColumnStatistics.featureGenerationReport = self.fg_handler.report

        # ------------------------ Dimensionality Reduction ------------------------ #
        data_encoded = self.post_processing_handler.fit_transform(data_encoded)

        # ------------------------ Store the feature order for use in transformation ------------------------ #
        self.fitted_config = self.fitted_config.copy(update={"output_feature_order": list(data_encoded.columns)})

        # ------------------------ Add the label column at the end------------------------ #
        data_encoded = data_encoded.join(encoded_label, how="inner")

        # ──────────────────────────── Reporting ───────────────────────────── #
        # Column count does not include label column
        self.report_builder.multiColumnStatistics.columnCountBeforePreprocessing = (
            len(self.fitted_config.original_columns) - 1
        )
        self.report_builder.multiColumnStatistics.columnCountAfterPreprocessing = len(data_encoded.columns) - 1
        self.report_builder.multiColumnStatistics.droppedColumns = len(self.feature_handler.removed_cols)

        logger.info(" Preprocess Test Set ".center(60, "-"))
        logger.info(f"→ forming {data_encoded.shape[1]} encoded features")

        return data_encoded

    def _drop_anomaly_rows(self, data: pd.DataFrame, label_name: str) -> Tuple[pd.DataFrame, int]:
        """Remove rows that are considered anomalies.
        Args:
            data (pd.DataFrame):
                data to remove anomalies from
            label_name (str):
                name of the label column
        Returns:
            pd.DataFrame:
                data without anomalies
        """
        # ---------------------- no removal for regression and forecasting ---------------------- #

        if self.config.ml_task is not MlTask.classification or self.config.is_time_series:
            return data, 0

        # by default value_counts() does not include NaN values, setting dropna=False includes them
        class_counts = data[label_name].value_counts(dropna=False)

        # ------------------------ drop missing values below a threshold ------------------------ #

        # Detect the indexes of null labels
        mask_missing_labels = data[label_name].isnull()
        n_rows = data.shape[0]
        n_missing = mask_missing_labels.sum()

        if n_missing > 0 and n_missing < int(CONF.LABEL_MISSING_THRESHOLD * len(data)) and len(class_counts) > 2:
            data.drop(data[mask_missing_labels].index, inplace=True)
            self.fitted_config = self.fitted_config.copy(update={"drop_missing_labels": True})

        # ------------------------ drop classes where unique_vales < 5 ------------------------ #

        # --- Check if the label column is unbalanced and drop rows with imbalanced classes --- #

        # Create a boolean mask to identify values that occur at least 5 times
        contains_imbalanced = class_counts < 5

        # Count the imbalanced classes and the remaining classes
        n_imbalanced = len(class_counts[contains_imbalanced])
        remaining_classes = len(class_counts) - n_imbalanced

        # if it is a multi-class classification task and there are any values occurring less than 5 times
        # if there are more than 2 classes, then drop the rows with these values
        if n_imbalanced > 0 and remaining_classes > 1:
            # Use the boolean mask to filter the original series
            mask_imbalanced_classes = data[self.config.label_column].isin(class_counts[contains_imbalanced].index)

            # Drop rows with imbalanced classes
            data.drop(data[mask_imbalanced_classes].index, inplace=True)

            # Set the unbalanced classes flag for transform
            self.fitted_config = self.fitted_config.copy(
                update={"dropped_imbalanced_classes": class_counts[contains_imbalanced].keys().to_list()}
            )

            # warn users that some classes have been dropped
            logger.warning(
                f"→ The following classes have been dropped due to unbalanced classes: {self.fitted_config.dropped_imbalanced_classes}"
            )

        # -------------------------------------- logging -------------------------------------- #

        # find number of missing rows
        if data.shape[0] < n_rows:
            n_missing = n_rows - data.shape[0]

        return data, n_missing

    def get_requirements_extras(self) -> Tuple[str, List[str]]:
        """Gets the requirements for this preprocessor as a pair
        (library_version, extras).
        """
        # Get the library version from a util function
        library_version = _py_version()

        # Figure out which extras will be required to preprocess the same data again
        # --------------------------------------
        # - Some dataset require importing expensive (size & import time) libraries
        # - We need to know if those libraries will be needed
        #   => every library behind an extra should be lazy imported (behind if statements)
        #   => imports happen for encoding
        # - We use extras to control installation of those libraries
        # - We're building an artifact targeting a specific dataset
        #   => we can know exactly which library will be needed or not

        removed_cols = self.feature_handler.removed_cols  # Removed cols are not encoded
        unique_types = set(
            [
                col_info.detectedType.value
                for col_info in self.config.info_map.values()
                if col_info.name not in removed_cols
            ]
        )

        # Extras are detected types that have an associated requirements file (e.g. not int)
        extras = [detected_type for detected_type in unique_types if detected_type in conf_mgr.requirements_map]

        # If all existing extras are required, we can use 'all' for simplicity
        if len(conf_mgr.requirements_map) == len(extras):
            extras = ["all"]

        return library_version, extras

    def save_requirements(self, path: Path) -> None:
        """Save all the preprocessed model requirements in one file."""
        library_version, extras = self.get_requirements_extras()
        extras_str = f"[{','.join(extras)}]" if extras else ""

        path.write_text(f"evoml_preprocessor{extras_str}=={library_version}\n")

    def save_joblib(self, path: Path) -> None:
        """Saves this object to the file-system.
        Args:
            path (Path):
                path to save the joblib file
        Returns:
            None
        """
        super().remove_nonpickled_attributes()
        external_preprocessor: DataPreprocessor = DataPreprocessor(
            config=self.config,
            label_handler=self.label_handler,
            index_handler=self.index_handler,
            feature_handler=self.feature_handler,
            fs_handler=self.fs_handler,
            fg_handler=self.fg_handler,
            data_preparation_handler=self.data_preparation_handler,
            post_processing_handler=self.post_processing_handler,
            fitted_config=self.fitted_config,
        )
        external_preprocessor.__dict__.update(self.__dict__)
        joblib.dump(external_preprocessor, path)


if __name__ == "__main__":
    pass
