from networksecurity.exception.exception import NetworkSecurityException
import networksecurity.logging as logger
from networksecurity.entity.constant_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifacts
from networksecurity.entity.constant_entity import TrainingPipelineConfig

import os
import sys
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import pymongo
from typing import List
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Read Data from MongoDb
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], inplace=True, axis=1)
            df.replace({"na":np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, df: pd.DataFrame):
        """
        Export RAW data to feature store
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = self.data_ingestion_config.feature_store_dir
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Split RAW data to train and test sets
        """
        try:
            train_data, test_data = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logger.logging.info("Train and Test Split on the Dataframe")
            dir_name = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_name, exist_ok=True)
            train_data.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            dir_name = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(dir_name, exist_ok=True)
            test_data.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logger.logging.info("Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        """
        Initiate the all the processes
        """
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifacts = DataIngestionArtifacts(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        


if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config)
    logger.logging.info("Intiate data ingestion")
    data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifacts)