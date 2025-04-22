import sys
import os
import networksecurity.logging as logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.constant_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from networksecurity.entity.artifacts_entity import (
    DataIngestionArtifacts,
    DataValidationArtifacts,
    DataTransformationArtifacts,
    ModelTrainerArtifact
)
from networksecurity.entity.constant_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config)
            logger.logging.info("Intiate data ingestion")
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logger.logging.info("Data ingestion completed")
            logger.logging.info(f"Data Ingestion Artifacts:\n{data_ingestion_artifacts}")
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifacts: DataIngestionArtifacts):
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifacts, data_validation_config)
            logger.logging.info("Initiated data validation")
            data_validation_artifacts = data_validation.initiate_data_validation_config()
            logger.logging.info("Data validation completed")
            logger.logging.info(f"Data Validation Artifacts:\n{data_validation_artifacts}")
            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(self, data_validation_artifacts: DataValidationArtifacts):
        try:
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifacts, data_transformation_config)
            logger.logging.info("Initiate data transformation")
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            logger.logging.info("Data transformation completed")
            logger.logging.info(f"Data Transformation Artifacts:\n{data_transformation_artifacts}")
            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_training(self, data_transformation_artifacts: DataTransformationArtifacts):
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifacts, model_trainer_config)
            logger.logging.info("Initiate Model Training")
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logger.logging.info("Model training completed")
            logger.logging.info(f"Model Trainer Artifacts:\n{model_trainer_artifacts}")
            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifacts = self.start_data_transformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts = self.start_model_training(data_transformation_artifacts=data_transformation_artifacts)
            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)