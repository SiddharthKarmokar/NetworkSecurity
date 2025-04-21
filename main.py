from networksecurity.entity.artifacts_entity import DataIngestionArtifacts, DataValidationArtifacts
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.constant_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
import networksecurity.logging as logger


if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config)
    logger.logging.info("Intiate data ingestion")
    data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
    logger.logging.info("Data ingestion completed")
    print(data_ingestion_artifacts)
    logger.logging.info("Initiated data validation")
    data_validation_config = DataValidationConfig(training_pipeline_config)
    data_validation = DataValidation(data_ingestion_artifacts, data_validation_config)
    data_validation_artifacts = data_validation.initiate_data_validation_config()
    logger.logging.info("Data validation completed")
    print(data_validation_artifacts)