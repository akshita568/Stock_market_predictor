import os
import sys
import pandas as pd
import yfinance as yf

from src.logging.logger import logging
from src.exception.exception import StockPredictorException


class DataIngestion:

    def __init__(
        self,
        # Shifted default start to 2024 for a lightweight, modern dataset
        start_date="2024-01-01",
        end_date=None,
        output_path="notebooks/artifacts/stock_data.csv"
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.output_path = output_path

    def initiate_data_ingestion(self):
        try:
            logging.info("Fetching S&P 500 company list from Wikipedia...")
            
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            tables = pd.read_html(url, storage_options=headers)
            tickers = tables[0]["Symbol"].tolist()

            # Yahoo Finance adjustments (e.g., BRK.B becomes BRK-B)
            tickers = [ticker.replace(".", "-") for ticker in tickers]

            logging.info(f"Downloading recent historical data for {len(tickers)} companies from {self.start_date}...")

            # Download all data in one giant multi-threaded batch
            df = yf.download(
                tickers=tickers,
                start=self.start_date,
                end=self.end_date,
                interval="1d",
                auto_adjust=False,
                threads=True,
                progress=True
            )

            if df.empty:
                raise Exception("Downloaded dataframe is empty.")

            logging.info("Reshaping dataframe using modern pandas stacking...")

            # Flatten multi-index cleanly into rows
            final_df = df.stack(level=1, future_stack=True)
            final_df = final_df.reset_index()
            
            # Sanitize headers to match standard lowercase layout
            final_df.columns = [col.lower() for col in final_df.columns]
            final_df.rename(columns={'ticker': 'symbol'}, inplace=True)

            # Directory safety handling for running inside Notebooks vs Root terminal
            actual_output_path = self.output_path
            if os.getcwd().endswith("notebooks") and actual_output_path.startswith("notebooks/"):
                actual_output_path = actual_output_path.replace("notebooks/", "", 1)

            # Ensure local artifact directory exists
            os.makedirs(os.path.dirname(actual_output_path), exist_ok=True)
            
            # Save final dataset
            final_df.to_csv(actual_output_path, index=False)

            logging.info(f"Dataset shape: {final_df.shape}")
            logging.info(f"Recent data successfully saved to: {actual_output_path}")
            return final_df

        except Exception as e:
            raise StockPredictorException(e, sys)