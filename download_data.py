import os
import pandas as pd
import yfinance as yf

# Create data folder
os.makedirs("data", exist_ok=True)

stocks = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Google",
    "AMZN": "Amazon",
    "TSLA": "Tesla",
    "META": "Meta",
    "NVDA": "Nvidia",
    "RELIANCE.NS": "Reliance",
    "TCS.NS": "TCS",
    "INFY.NS": "Infosys"
}

for ticker, company in stocks.items():

    print(f"Downloading {company} ({ticker})...")

    df = yf.download(
        ticker,
        start="2015-01-01",
        end="2025-01-01",
        auto_adjust=False,
        progress=False,
        multi_level_index=False
    )

    # Flatten columns if your yfinance version still returns MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Make Date a normal column
    df = df.reset_index()

    # Add company symbol
    df["Symbol"] = ticker

    # Save
    filename = f"data/{ticker.replace('.', '_')}.csv"
    df.to_csv(filename, index=False)

    print(f"Saved -> {filename}")

print("\nAll datasets downloaded successfully!")