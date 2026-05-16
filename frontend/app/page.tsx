"use client";

import { useState } from "react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Home() {
  const [ticker, setTicker] = useState("");
  const [stockData, setStockData] = useState<any>(null);
  const [historyData, setHistoryData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function fetchStock() {
    if (!ticker) return;

    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/stocks/${ticker}`
      );

      const data = await response.json();
      
      setStockData(data);

      const historyResponse = await fetch(
        `http://127.0.0.1:8000/stocks/${ticker}/history`
      );

      const history = await historyResponse.json();

      setHistoryData(history.history);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  }

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <div className="max-w-5xl mx-auto">

        <h1 className="text-5xl font-bold mb-4">
          SignalFlow
        </h1>

        <p className="text-gray-400 text-lg mb-10">
          AI-powered financial intelligence platform
        </p>

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

        {loading && (
          <p className="text-gray-400">
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