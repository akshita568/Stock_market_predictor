import sys
import yfinance as yf
import pandas as pd
from src.logging.logger import logging
from src.exception.exception import StockPredictorException
from src.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> str:
        logging.info("Initiating historical stock data ingestion...")
        try:
            # Download ticker information
            stock = yf.Ticker(self.config.ticker)
            df = stock.history(start=self.config.start_date, end=self.config.end_date, interval="1d")
            
            if df.empty:
                raise ValueError(f"Ticker history returned empty for symbol: {self.config.ticker}")

            # Save clean CSV output to directory artifact destination
            df.reset_index(inplace=True)
            df.columns = [col.lower() for col in df.columns]
            
            output_file = self.config.download_path
            df.to_csv(output_file, index=False)
            logging.info(f" Ingestion completed. Clean artifact saved to {output_file}")
            
            return str(output_file)

        except Exception as e:
            raise StockPredictorException(e, sys)