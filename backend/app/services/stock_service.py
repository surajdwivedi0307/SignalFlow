import yfinance as yf


def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "ticker": ticker.upper(),
        "company_name": info.get("longName"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
    }
def get_stock_history(ticker: str, period: str = "1mo"):
    stock = yf.Ticker(ticker)

    history = stock.history(period=period)

    data = []

    for date, row in history.iterrows():
        data.append({
            "date": str(date.date()),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        })

    return {
        "ticker": ticker.upper(),
        "period": period,
        "history": data
    }