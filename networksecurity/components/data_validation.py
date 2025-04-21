from networksecurity.entity.artifacts_entity import DataIngestionArtifacts, DataValidationArtifacts
from networksecurity.entity.constant_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_NAME
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import read_yaml, write_yaml
import networksecurity.logging as logger
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(self, data_ingestion_artifacts: DataIngestionArtifacts, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_NAME)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_csv(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame):
        try:
            number_of_columns = len(self._schema_config)
            if len(dataframe) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column : {
                        "p_value" : float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml(file_path=drift_report_file_path, content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation_config(self):
        try:
            train_file_path = self.data_ingestion_artifacts.train_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path

            train_dataframe = self.read_csv(train_file_path)
            test_dataframe = self.read_csv(test_file_path)

            error_message = ""
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all the columns.\n"
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message += f"Test dataframe does not contain all the columns.\n"
            
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_data_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_data_file_path, index=False, header=True
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_data_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifacts(
                drift_status=status,
                valid_train_file_path=self.data_validation_config.valid_test_data_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_data_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)