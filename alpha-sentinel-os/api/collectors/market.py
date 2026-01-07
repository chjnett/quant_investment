# Market Data Collector (yfinance)
import yfinance as yf

def fetch_ticker_data(ticker):
    return yf.Ticker(ticker).history()
