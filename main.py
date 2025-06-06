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
import networksecurity.logging as logger


if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config)
    logger.logging.info("Intiate data ingestion")
    data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
    logger.logging.info("Data ingestion completed")
    print(data_ingestion_artifacts)

    data_validation_config = DataValidationConfig(training_pipeline_config)
    data_validation = DataValidation(data_ingestion_artifacts, data_validation_config)
    logger.logging.info("Initiated data validation")
    data_validation_artifacts = data_validation.initiate_data_validation_config()
    logger.logging.info("Data validation completed")
    print(data_validation_artifacts)
    
    data_transformation_config = DataTransformationConfig(training_pipeline_config)
    data_transformation = DataTransformation(data_validation_artifacts, data_transformation_config)
    logger.logging.info("Initiate data transformation")
    data_transformation_artifacts = data_transformation.initiate_data_transformation()
    logger.logging.info("Data transformation completed")
    print(data_transformation_artifacts)

    model_trainer_config = ModelTrainerConfig(training_pipeline_config)
    model_trainer = ModelTrainer(data_transformation_artifacts, model_trainer_config)
    logger.logging.info("Initiate Model Training")
    model_trainer_artifacts = model_trainer.initiate_model_trainer()
    logger.logging.info("Model training completed")
    print(model_trainer_artifacts)