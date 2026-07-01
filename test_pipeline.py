import sys
import os
from pathlib import Path

# Add current working directory to sys.path to allow relative src imports easily
sys.path.append(os.getcwd())

from src.logging.logger import logging
from src.exception.exception import StockPredictorException
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import DataIngestionConfig
from src.components.data_ingestion import DataIngestion

def run_verification():
    try:
        logging.info(" Verification script started.")
        
        # 1. Test Utility: Load YAML configuration
        config_path = Path("test_config.yaml")
        config_dict = read_yaml(config_path)
        print("✓ Step 1: YAML configurations parsed successfully.")
        
        # 2. Test Utility: Dynamic Directory Generation
        create_directories([
            config_dict['artifacts']['root_dir'],
            config_dict['artifacts']['data_ingestion_dir']
        ])
        print("✓ Step 2: Directories created cleanly.")
        
        # 3. Test Entity: Instantiate Data Ingestion Config Contract
        ingestion_config = DataIngestionConfig(
            root_dir=Path(config_dict['artifacts']['root_dir']),
            ticker=config_dict['project']['ticker'],
            start_date=config_dict['project']['start_date'],
            end_date=config_dict['project']['end_date'],
            download_path=Path(config_dict['artifacts']['raw_data_file'])
        )
        print("✓ Step 3: Config DataClass instantiated safely.")
        
        # 4. Test Component: Execute Data Collection
        ingestion_engine = DataIngestion(config=ingestion_config)
        saved_file_path = ingestion_engine.initiate_data_ingestion()
        
        print(f"\n SUCCESS! Everything ran smoothly.")
        print(f"Data file downloaded to: {saved_file_path}")
        print(" Logs have been appended inside the 'logs/' folder.")
        
    except Exception as e:
        # Testing if our global custom exception structure catches failures beautifully
        raise StockPredictorException(e, sys)

if __name__ == "__main__":
    run_verification()