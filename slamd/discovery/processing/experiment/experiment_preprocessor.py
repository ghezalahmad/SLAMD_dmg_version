from slamd.common.error_handling import SequentialLearningException, ValueNotSupportedException, \
    SlamdUnprocessableEntityException
from slamd.discovery.processing.experiment.experiment_model import ExperimentModel


class ExperimentPreprocessor:

    @classmethod
    def preprocess(cls, exp):
        cls.filter_apriori_with_thresholds_and_update_orig_data(exp)
        cls.filter_missing_inputs(exp)
        cls.validate_experiment(exp)
        cls.encode_categoricals(exp)

    @classmethod
    def validate_experiment(cls, exp):
        cls._validate_user_input(exp)
        cls._validate_target_labels(exp)

    @classmethod
    def _validate_user_input(cls, exp):
        if exp.model not in ExperimentModel.get_all_models():
            raise ValueNotSupportedException(message=f'Invalid model: {exp.model}')

        if len(exp.target_names) == 0:
            raise SequentialLearningException('No targets were specified!')

        if len(exp.feature_names) == 0:
            raise SequentialLearningException('No features specified or all features dropped due to nan values')

        if not (len(exp.target_names) == len(exp.target_weights) == len(exp.target_thresholds) ==
                len(exp.target_max_or_min)):
            raise SlamdUnprocessableEntityException(message='Target names, weights, thresholds, and max_or_min '
                                                            'parameters do not have the same length.')
        if not (len(exp.apriori_names) == len(exp.apriori_weights) == len(exp.apriori_thresholds) ==
                len(exp.apriori_max_or_min)):
            raise SlamdUnprocessableEntityException(message='Apriori names, weights, thresholds, and max_or_min '
                                                            'parameters do not have the same length.')

        for value in exp.target_max_or_min + exp.apriori_max_or_min:
            if value not in ['min', 'max']:
                raise SequentialLearningException(f'Invalid value for max_or_min, got {value}')

        if exp.model in ExperimentModel.get_tuned_models() and len(exp.target_names) > 1:
            raise ValueNotSupportedException(
                message=f'{exp.model} only supports one target column, got {len(exp.target_names)}')

    @classmethod
    def _validate_target_labels(cls, exp):
        for target, count in zip(exp.target_names, exp.targets_df.count()):
            if exp.model == ExperimentModel.RANDOM_FOREST.value and count <= 1:
                raise ValueNotSupportedException(
                    message=f'Not enough labelled values for target: {target}. The Random Forest Regressor '
                            f'requires at least 2 labelled values, but only {count} was/were found. '
                            f'Please ensure that there are at least 2 data points that are not filtered out '
                            f'by the a priori thresholds.'
                )
            if exp.model == ExperimentModel.GAUSSIAN_PROCESS.value and count < 1:
                raise ValueNotSupportedException(
                    message=f'Not enough labelled values for target: {target}. The Gaussian Process Regressor '
                            f'requires at least 1 labelled value, but none were found. '
                            f'Please ensure that there is at least 1 data point that is not filtered out '
                            f'by the a priori information thresholds.'
                )
            if exp.model in ExperimentModel.get_tuned_models() and count < 4:
                raise ValueNotSupportedException(
                    message=f'Not enough labelled values for target: {target}. The {exp.model} model '
                            f'requires at least 4 labelled values, but only {count} was/were found. '
                            f'Please ensure that there are at least 4 data points that are not filtered out '
                            f'by the a priori thresholds.'
                )
            if count == len(exp.targets_df.index):
                raise SequentialLearningException(message=f'All data is already labelled for target {target}.')

    @classmethod
    def encode_categoricals(cls, exp):
        non_numeric_features = exp.features_df.select_dtypes(exclude='number').columns

        for feature in non_numeric_features:
            exp.dataframe[feature], _ = exp.dataframe[feature].factorize()

    @classmethod
    def filter_missing_inputs(cls, exp):
        for col in exp.feature_names.copy():
            if exp.dataframe[col].isna().values.any():
                exp.dataframe.drop(col, axis=1, inplace=True)
                exp.feature_names.remove(col)

    @classmethod
    def filter_apriori_with_thresholds_and_update_orig_data(cls, exp):
        # In the future this function could be handled "live" and non-destructively in index_all_labelled and index_none_labelled
        for (column, value, threshold) in zip(exp.apriori_names, exp.apriori_max_or_min, exp.apriori_thresholds):
            if threshold is None:
                continue

            # index of rows in which all target columns are nan
            nodata_index = exp.targets_df.isna().all(axis=1)
            if value == 'max':
                # Get dataframe mask based on threshold value and nodata_index.
                # Apply mask to dataframe. Get index of values to drop.
                # Use new index to drop values from original dataframe.
                exp.dataframe.drop(
                    exp.dataframe[(exp.dataframe[column] < threshold) & nodata_index].index,
                    inplace=True
                )
            else:
                exp.dataframe.drop(
                    exp.dataframe[(exp.dataframe[column] > threshold) & nodata_index].index,
                    inplace=True
                )

        exp.dataframe.reset_index(drop=True, inplace=True)
        exp.orig_data = exp.dataframe.copy()
