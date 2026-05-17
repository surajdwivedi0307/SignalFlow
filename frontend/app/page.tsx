"use client";

import { useState, useEffect } from "react";

export default function Home() {

  const [ticker, setTicker] = useState("");

  const [stockData, setStockData] = useState<any>(null);

  const [portfolioData, setPortfolioData] = useState<any>(null);

  const [loading, setLoading] = useState(false);

  async function fetchStock() {

    if (!ticker) return;

    setLoading(true);

    try {

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/stocks/${ticker}`
      );

      const data = await response.json();

      setStockData(data);

    } catch (error) {

      console.error(error);

    }

    setLoading(false);
  }

  async function fetchPortfolioSummary() {

    try {

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/portfolio/1/summary`
      );

      const data = await response.json();

      setPortfolioData(data);

    } catch (error) {

      console.error(error);

    }
  }

  useEffect(() => {

    fetchPortfolioSummary();

  }, []);

  return (

    <main className="min-h-screen bg-black text-white p-10">

      <div className="max-w-6xl mx-auto">

        <h1 className="text-5xl font-bold mb-4">
          SignalFlow
        </h1>

        <p className="text-zinc-400 text-lg mb-10">
          AI-powered portfolio intelligence platform
        </p>

        {/* Portfolio Intelligence Dashboard */}

        {portfolioData && (

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">

            {/* Portfolio Health */}

            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">

              <p className="text-zinc-400 mb-2">
                Portfolio Health
              </p>

              <h2 className="text-5xl font-bold mb-3">
                {portfolioData.portfolio_health_score}/100
              </h2>

              <p className="text-xl">
                {portfolioData.health_status}
              </p>

            </div>

            {/* Risk Summary */}

            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">

              <p className="text-zinc-400 mb-2">
                Risk Level
              </p>

              <h2 className="text-4xl font-bold mb-3">
                {portfolioData.risk_level}
              </h2>

              <p className="text-zinc-300">
                {portfolioData.risk_reason}
              </p>

            </div>

          </div>
        )}

        {/* Attention Insights */}

        {portfolioData && (

          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 mb-10">

            <h2 className="text-2xl font-bold mb-6">
              Attention Insights
            </h2>

            <div className="space-y-4">

              {portfolioData.attention_insights.map(
                (insight: string, index: number) => (

                  <div
                    key={index}
                    className="bg-zinc-800 rounded-xl p-4"
                  >
                    {insight}
                  </div>
                )
              )}

            </div>

          </div>
        )}

        {/* Holdings Table */}

        {portfolioData && (

          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 mb-10 overflow-auto">

            <h2 className="text-2xl font-bold mb-6">
              Portfolio Holdings
            </h2>

            <table className="w-full">

              <thead>

                <tr className="text-left text-zinc-400 border-b border-zinc-800">

                  <th className="pb-3">Ticker</th>

                  <th className="pb-3">Allocation</th>

                  <th className="pb-3">Current Value</th>

                  <th className="pb-3">Profit / Loss</th>

                </tr>

              </thead>

              <tbody>

                {portfolioData.holdings.map((holding: any) => (

                  <tr
                    key={holding.ticker}
                    className="border-b border-zinc-800"
                  >

                    <td className="py-4 font-semibold">
                      {holding.ticker}
                    </td>

                    <td className="py-4">
                      {holding.allocation_percent}%
                    </td>

                    <td className="py-4">
                      ${holding.current_value}
                    </td>

                    <td className="py-4">
                      ${holding.profit_loss}
                    </td>

                  </tr>
                ))}

              </tbody>

            </table>

          </div>
        )}

        {/* Stock Search */}

        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 mb-6">

          <h2 className="text-2xl font-semibold mb-4">
            Stock Search
          </h2>

          <div className="flex gap-4">

            <input
              type="text"
              placeholder="Enter ticker (AAPL)"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              className="bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-3 w-full"
            />

            <button
              onClick={fetchStock}
              className="bg-white text-black px-6 py-3 rounded-lg font-semibold"
            >
              Search
            </button>

          </div>

        </div>

        {/* Stock Details */}

        {loading && (

          <p className="text-zinc-400">
            Loading...
          </p>
        )}

        {stockData && (

          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">

            <h2 className="text-3xl font-bold mb-4">
              {stockData.company_name}
            </h2>

            <div className="space-y-2 text-lg">

              <p>
                Ticker: {stockData.ticker}
              </p>

              <p>
                Current Price: ${stockData.current_price}
              </p>

              <p>
                Market Cap: {stockData.market_cap}
              </p>

              <p>
                Sector: {stockData.sector}
              </p>

              <p>
                Industry: {stockData.industry}
              </p>

            </div>

          </div>
        )}

      </div>

    </main>
  );
}