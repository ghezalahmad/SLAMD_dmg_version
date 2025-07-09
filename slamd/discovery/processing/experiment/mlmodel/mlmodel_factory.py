import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.experiment.mlmodel.slamd_random_forest import SlamdRandomForest
from slamd.discovery.processing.experiment.mlmodel.tuned_gaussian_process_regressor import TunedGaussianProcessRegressor
from slamd.discovery.processing.experiment.mlmodel.tuned_random_forest import TunedRandomForest
from slamd.discovery.processing.experiment.experiment_model import ExperimentModel
import os


# Ensure Lolo jar path is available for lolopy
os.environ['LOLO_JAR_PATH'] = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'libs', 'lolo-0.7.3.jar')


class MLModelFactory:

    @classmethod
    def initialize_model(cls, exp):
        """
        Initialize the model given by the user. Return a sklearn Regressor.
        The model must be one of the entries defined in ExperimentModel.
        """
      
        if exp.model == ExperimentModel.RANDOM_FOREST.value:
            logger.info("🧪 Preprocessing data for Lolo Random Forest")

            # Use only rows where target is not null
            index_labelled = exp.targets_df.index[exp.targets_df[exp.target_names[0]].notnull()]
            X_df = exp.features_df.loc[index_labelled]
            y_series = exp.targets_df.loc[index_labelled, exp.target_names[0]]

            logger.info(f"🧾 Features shape: {X_df.shape}, Target shape: {y_series.shape}")
            logger.info(f"🔍 Feature dtypes:\n{X_df.dtypes}")

            if X_df.isnull().values.any() or y_series.isnull().values.any():
                raise ValueError("❌ Dataset contains NaN values. Lolo cannot proceed.")

            try:
                X_np = X_df.astype(np.float64).to_numpy()
                y_np = y_series.astype(np.float64).to_numpy()
            except Exception as e:
                logger.error("❌ Data type conversion failed", exc_info=True)
                raise ValueError(f"Failed to convert data to float64: {e}")

            # Inject into experiment so SlamdRandomForest can use it
            exp.X_np = X_np
            exp.y_np = y_np

            logger.info("✅ Data ready for Lolo Random Forest")

            # ✅ IMPORTANT: pass the experiment object here
            regressor = SlamdRandomForest()



        elif exp.model == ExperimentModel.GAUSSIAN_PROCESS.value:
            # Hyperparameters from previous implementation of the app (Jupyter notebook).
            kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
            regressor = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9, random_state=42)
        elif exp.model == ExperimentModel.PCA_GAUSSIAN_PROCESS.value:
            # These hyperparameters were found to be potentially interesting by running local experiments.
            predictor = GaussianProcessRegressor(n_restarts_optimizer=3, random_state=42)
            pca = PCA(n_components=0.99)
            regressor = Pipeline([('pca', pca), ('pred', predictor)])
        elif exp.model == ExperimentModel.PCA_RANDOM_FOREST.value:
            predictor = SlamdRandomForest()
            pca = PCA(n_components=0.99)
            regressor = Pipeline([('pca', pca), ('pred', predictor)])
        elif exp.model in ExperimentModel.get_tuned_models():
            # These models only support one target for now. Validated user input in ExperimentPreprocessor.
            target = exp.target_names[0]
            index_labelled = exp.targets_df.index[exp.targets_df[target].notnull()]
            training_rows = exp.features_df.loc[index_labelled].values
            training_labels = exp.targets_df.loc[index_labelled, target].values.reshape(-1, 1)

            if exp.model == ExperimentModel.TUNED_GAUSSIAN_PROCESS.value:
                regressor = TunedGaussianProcessRegressor.find_best_model(training_rows, training_labels)
            else:
                regressor = TunedRandomForest.find_best_model(training_rows, training_labels)
        else:
            raise ValueNotSupportedException(message=f'Invalid model: {exp.model}')

        return regressor


import logging
logger = logging.getLogger(__name__)

def initialize_model(experiment):
    logger.info(f"🚀 Initializing model: {experiment.regressor}")
    if experiment.regressor == 'random_forest':
        from lolopy.learners import RandomForestRegressor
        logger.info("✅ RandomForestRegressor from lolopy triggered.")
        return SlamdRandomForest()
