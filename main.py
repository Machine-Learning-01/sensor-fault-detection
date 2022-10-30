from sensor.pipeline.train_pipeline import TrainPipeline

pipeline = TrainPipeline()

data_ingestion_artifact = pipeline.start_data_ingestion()

data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)