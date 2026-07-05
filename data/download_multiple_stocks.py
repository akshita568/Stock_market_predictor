import os
import yfinance as yf

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# List of stock symbols
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
        progress=False
    )

    filename = f"data/{ticker.replace('.', '_')}.csv"
    df.to_csv(filename)

    print(f"Saved -> {filename}")

print("\nAll datasets downloaded successfully!")