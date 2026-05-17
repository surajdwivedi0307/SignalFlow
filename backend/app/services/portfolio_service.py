import yfinance as yf

from app.models.portfolio_snapshot import (
    PortfolioSnapshot
)


def get_current_price(ticker: str):

    stock = yf.Ticker(ticker)

    history = stock.history(period="1d")

    if history.empty:

        return None

    return round(
        history["Close"].iloc[-1],
        2
    )


def generate_portfolio_narrative(

    risk_level,

    diversification_status,

    health_status,

    attention_insights

):

    narrative = ""

    # risk interpretation

    if risk_level == "HIGH":

        narrative += (
            "Your portfolio currently has "
            "high concentration risk. "
        )

    elif risk_level == "MEDIUM":

        narrative += (
            "Your portfolio has moderate "
            "concentration risk. "
        )

    else:

        narrative += (
            "Your portfolio risk profile "
            "appears balanced. "
        )

    # diversification interpretation

    if diversification_status == (
        "Poorly Diversified"
    ):

        narrative += (
            "Diversification remains weak "
            "across holdings. "
        )

    elif diversification_status == (
        "Moderately Diversified"
    ):

        narrative += (
            "Portfolio diversification "
            "is improving. "
        )

    else:

        narrative += (
            "Portfolio diversification "
            "looks healthy. "
        )

    # health interpretation

    narrative += (
        f"Overall portfolio health is "
        f"classified as {health_status}. "
    )

    # attention insights

    if len(attention_insights) > 0:

        narrative += (
            "Key portfolio observations: "
        )

        narrative += (
            ". ".join(attention_insights[:2])
        )

        narrative += "."

    return narrative

def calculate_portfolio_summary(
    portfolio,
    db
):
    total_invested = 0.0
    total_current_value = 0.0
    holdings_summary = []

    for holding in portfolio.holdings:
        current_price = get_current_price(holding.ticker)
        if current_price is None:
            continue

        invested_value = float(holding.quantity * holding.buy_price)
        current_value = float(holding.quantity * current_price)
        profit_loss = float(current_value - invested_value)

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
            "allocation_percent": 0.0,
        })

    total_profit_loss = total_current_value - total_invested
    largest_holding = None
    largest_allocation = 0.0
    diversification_score = 100
    diversification_status = "Well Diversified"
    attention_insights = []
    risk_level = "LOW"
    risk_reason = "Portfolio appears diversified"

    defensive_stocks = [
        "KO",
        "PG",
        "JNJ"
    ]

    for holding in holdings_summary:
        if total_current_value == 0:
            allocation_percent = 0.0
        else:
            allocation_percent = (
                holding["current_value"] /
                total_current_value
            ) * 100

        holding["allocation_percent"] = round(allocation_percent, 2)

        if allocation_percent > largest_allocation:
            largest_allocation = allocation_percent
            largest_holding = holding["ticker"]

        if allocation_percent > 50:
            diversification_score = 20
            diversification_status = "Poorly Diversified"
        elif allocation_percent > 30:
            diversification_score = 55
            diversification_status = "Moderately Diversified"
        elif allocation_percent > 15:
            diversification_score = 80
            diversification_status = "Reasonably Diversified"

        if allocation_percent > 40:
            risk_level = "HIGH"
            risk_reason = (
                f'{holding["ticker"]} exceeds '
                '40% portfolio allocation'
            )
        elif allocation_percent > 25 and risk_level != "HIGH":
            risk_level = "MEDIUM"
            risk_reason = (
                f'{holding["ticker"]} has elevated '
                'portfolio concentration'
            )

        if allocation_percent > 30:
            attention_insights.append(
                f'{holding["ticker"]} represents '
                f'{round(allocation_percent, 1)}% '
                'of portfolio exposure'
            )

        if holding["ticker"] in defensive_stocks:
            attention_insights.append(
                f'{holding["ticker"]} adds '
                'defensive diversification'
            )

    tech_tickers = [
        "AAPL",
        "MSFT",
        "NVDA",
        "TSLA"
    ]
    tech_allocation = sum(
        holding["allocation_percent"]
        for holding in holdings_summary
        if holding["ticker"] in tech_tickers
    )

    if tech_allocation > 50:
        attention_insights.append(
            'Portfolio is heavily concentrated '
            'in growth and technology stocks'
        )

    portfolio_health_score = 100
    if risk_level == "HIGH":
        portfolio_health_score -= 35
    elif risk_level == "MEDIUM":
        portfolio_health_score -= 20

    if diversification_score == 20:
        portfolio_health_score -= 30
    elif diversification_score == 55:
        portfolio_health_score -= 15

    defensive_count = sum(
        1 for holding in holdings_summary
        if holding["ticker"] in defensive_stocks
    )
    portfolio_health_score += defensive_count * 5
    portfolio_health_score = max(0, min(portfolio_health_score, 100))

    if portfolio_health_score >= 80:
        health_status = "Excellent"
    elif portfolio_health_score >= 65:
        health_status = "Healthy"
    elif portfolio_health_score >= 45:
        health_status = "Needs Attention"
    else:
        health_status = "High Risk"

    portfolio_narrative = generate_portfolio_narrative(
        risk_level,
        diversification_status,
        health_status,
        attention_insights
    )

    snapshot = PortfolioSnapshot(
        portfolio_id=portfolio.id,
        portfolio_health_score=float(portfolio_health_score),
        total_value=float(total_current_value),
        risk_level=risk_level,
        diversification_score=float(diversification_score)
    )

    db.add(snapshot)
    db.commit()

    return {
        "portfolio_name": portfolio.name,
        "total_invested": round(total_invested, 2),
        "total_current_value": round(total_current_value, 2),
        "total_profit_loss": round(total_profit_loss, 2),
        "largest_holding": largest_holding,
        "risk_level": risk_level,
        "risk_reason": risk_reason,
        "diversification_score": diversification_score,
        "diversification_status": diversification_status,
        "attention_insights": attention_insights,
        "portfolio_health_score": portfolio_health_score,
        "health_status": health_status,
        "portfolio_narrative": portfolio_narrative,
        "holdings": holdings_summary,
    }

