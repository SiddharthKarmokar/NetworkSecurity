import sys
import os
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import mlflow

import networksecurity.logging as logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.constant_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array
from networksecurity.entity.artifacts_entity import ClassificationMetricArtifact
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel, evaluate_models
from networksecurity.entity.artifacts_entity import (
    DataTransformationArtifacts,
    ModelTrainerArtifact
)


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifacts, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def track_mlflow(self, best_model, classification_metrics: ClassificationMetricArtifact):
        with mlflow.start_run():
            f1_score = classification_metrics.f1_score
            precision_score = classification_metrics.precision_score
            recall_score = classification_metrics.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(best_model, "model")


    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "AdaBoost": AdaBoostClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1)
        }
        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss']
            },
            "Random Forest": {
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            "Gradient Boosting": {
                'learning_rate': [.1, .01, .05, .001],
                'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            "Logistic Regression": {},
            "AdaBoost": {
                'learning_rate': [0.1, 0.01, 0.5, 0.001],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            }
        }
        model_report: dict = evaluate_models(x_train, y_train, x_test, y_test, models, params)

        best_model_score = float("-inf")
        best_model_name = None
        best_model_params = None

        for model_name, (score, params) in model_report.items():
            if score > best_model_score:
                best_model_score = score
                best_model_name = model_name
                best_model_params = params

        best_model = models[best_model_name]
        best_model.set_params(**best_model_params)
        best_model.fit(x_train, y_train)

        y_train_pred = best_model.predict(x_train)
        train_classification_metric = get_classification_score(y_train, y_train_pred)
        self.track_mlflow(best_model, train_classification_metric)

        y_test_pred = best_model.predict(x_test)
        test_classification_metric = get_classification_score(y_test, y_test_pred)
        self.track_mlflow(best_model, test_classification_metric)

        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
        
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        
        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, Network_Model)
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_model_artifact=train_classification_metric,
            test_model_artifact=test_classification_metric
        )
        logger.logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
        return model_trainer_artifact
    
    def initiate_model_trainer(self):
        try:
            train_df = load_numpy_array(self.data_transformation_artifact.transformed_train_file_path)
            test_df = load_numpy_array(self.data_transformation_artifact.transformed_test_file_path)
            x_train, y_train, x_test, y_test = (
                train_df[:, :-1],
                train_df[:, -1],
                test_df[:, :-1],
                test_df[:, -1]
            )
            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        