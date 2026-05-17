import yfinance as yf


def get_current_price(ticker: str):

    stock = yf.Ticker(ticker)

    history = stock.history(period="1d")

    if history.empty:
        return None

    return round(history["Close"].iloc[-1], 2)

def calculate_portfolio_summary(portfolio):

    total_invested = 0

    total_current_value = 0

    holdings_summary = []

    for holding in portfolio.holdings:

        current_price = get_current_price(holding.ticker)

        if current_price is None:
            continue

        invested_value = holding.quantity * holding.buy_price

        current_value = holding.quantity * current_price

        profit_loss = current_value - invested_value

        total_invested += invested_value

        total_current_value += current_value

        holdings_summary.append({
            "ticker": holding.ticker,
            "quantity": holding.quantity,
            "buy_price": holding.buy_price,
            "current_price": current_price,
            "invested_value": round(invested_value, 2),
            "current_value": round(current_value, 2),
            "profit_loss": round(profit_loss, 2),
            "allocation_percent": 0
            
        })

    total_profit_loss = (
        total_current_value - total_invested
    )
    
    largest_holding = None
    largest_allocation = 0
    risk_level = "LOW"
    risk_reason = "Portfolio appears diversified"
    for holding in holdings_summary:
        allocation_percent = (holding["current_value"] / total_current_value) * 100

        holding["allocation_percent"] = round(allocation_percent, 2)

        # update largest holding
        if allocation_percent > largest_allocation:
            largest_allocation = allocation_percent
            largest_holding = holding["ticker"]

        # determine risk level based on individual allocation
        if allocation_percent > 40:
            risk_level = "HIGH"
            risk_reason = (
                f'{holding["ticker"]} exceeds 40% portfolio allocation'
            )
        elif allocation_percent > 25 and risk_level != "HIGH":
            risk_level = "MEDIUM"
            risk_reason = (
                f'{holding["ticker"]} has elevated portfolio concentration'
            )

    return {
        "portfolio_name": portfolio.name,
        "total_invested": round(total_invested, 2),
        "total_current_value": round(total_current_value, 2),
        "total_profit_loss": round(total_profit_loss, 2),
        "largest_holding": largest_holding,
        "risk_level": risk_level,
        "risk_reason": risk_reason,
        "holdings": holdings_summary
    }

