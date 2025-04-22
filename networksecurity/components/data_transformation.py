import sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifacts_entity import DataValidationArtifacts, DataTransformationArtifacts
from networksecurity.entity.constant_entity import DataValidationConfig, DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
import networksecurity.logging as logger 
from networksecurity.utils.main_utils.utils import save_numpy_array, save_object


class DataTransformation:
    def __init__(self, data_validation_artifacts: DataValidationArtifacts, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_csv(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformation_object(self):
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logger.logging.info(f"Intialised KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_transformation(self):
        try:
            logger.logging.info("Started Data Transformation")
            train_df = self.read_csv(self.data_validation_artifacts.valid_train_file_path)
            test_df = self.read_csv(self.data_validation_artifacts.valid_test_file_path)
            
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df.replace(-1, 0)
            
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformation_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_df = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_df = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            
            save_numpy_array(self.data_transformation_config.transformed_train_file_path, train_df)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path, test_df)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            save_object("final_model/preprocessor.pkl", preprocessor_object)

            data_transformation_artifact = DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)