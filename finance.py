import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class IndianStockAnalyzer:
    def __init__(self):
        # Local map for sector peers (Standard NSE Tickers)
        self.sector_map = {
            "Technology": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
            "Financial Services": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
            "Consumer Defensive": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS"],
            "Energy": ["RELIANCE.NS", "ONGC.NS", "BPCL.NS", "IOC.NS"],
            "Automobile": ["TATAMOTORS.NS", "M&M.NS", "MARUTI.NS", "BAJAJ-AUTO.NS"]
        }

    def find_ticker(self, company_name):
        """Searches for the ticker and ensures it has the .NS suffix."""
        search = yf.Search(company_name, max_results=5)
        for result in search.quotes:
            symbol = result['symbol']
            # Prioritize National Stock Exchange (NSE) results
            if symbol.endswith(".NS"):
                return symbol
        # If no .NS found in top results, try appending it to the first result
        if search.quotes:
            first_symbol = search.quotes[0]['symbol'].split('.')[0]
            return f"{first_symbol}.NS"
        return None

    def get_stock_metrics(self, ticker_symbol):
        """Fetches metrics using history to ensure correct currency (INR)."""
        stock = yf.Ticker(ticker_symbol)
        
        # 1. Fetch 1-year history for high, low, and average calculations
        hist_1y = stock.history(period="1y")
        if hist_1y.empty:
            return None

        current_price = hist_1y['Close'].iloc[-1]
        high_52w = hist_1y['High'].max()
        low_52w = hist_1y['Low'].min()
        avg_12m = hist_1y['Close'].mean()

        # 2. Fetch fundamental data from info
        info = stock.info
        
        return {
            "Symbol": ticker_symbol,
            "Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Current Price (INR)": round(current_price, 2),
            "52W High": round(high_52w, 2),
            "52W Low": round(low_52w, 2),
            "12M Avg Price": round(avg_12m, 2),
            "PE Ratio": info.get("trailingPE"),
            "EPS": info.get("trailingEps")
        }

    def analyze(self, query):
        print(f"\n{'='*40}\nAnalyzing: {query}\n{'='*40}")
        
        # Step 1: Find Ticker
        ticker = self.find_ticker(query)
        if not ticker:
            print("Error: Could not find a valid NSE ticker.")
            return

        # Step 2: Get Metrics
        metrics = self.get_stock_metrics(ticker)
        if not metrics:
            print(f"Error: No historical data found for {ticker}.")
            return

        # Step 3: Compare Competitors
        print(f"\n[1] Fundamentals for {metrics['Name']}")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

        print(f"\n[2] Competitor Comparison (Sector: {metrics['Sector']})")
        peers = self.sector_map.get(metrics['Sector'], [])
        
        comp_data = []
        for p_ticker in peers:
            p_stock = yf.Ticker(p_ticker)
            p_info = p_stock.info
            comp_data.append({
                "Ticker": p_ticker,
                "Name": p_info.get("shortName", "N/A"),
                "PE Ratio": p_info.get("trailingPE", "N/A"),
                "Current Price": p_info.get("currentPrice", "N/A")
            })
        
        if comp_data:
            print(pd.DataFrame(comp_data).to_string(index=False))
        else:
            print("  No pre-defined competitors found for this sector.")

# --- Run Analysis ---
analyzer = IndianStockAnalyzer()
analyzer.analyze("Infosys")
