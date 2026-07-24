"""
Bot Dashboard – Live-Übersicht deiner Trades
"""
import os, csv, json
from flask import Flask, render_template, jsonify

app = Flask(__name__)
BOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRADE_LOG = os.path.join(r"C:\Users\xxx3v", "trades.csv")

def load_trades():
    trades = []
    if not os.path.exists(TRADE_LOG):
        return trades
    with open(TRADE_LOG, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["profit_usd"] = float(row.get("profit_usd", 0))
                row["roi_pct"] = float(row.get("roi_pct", 0))
                row["slippage_pct"] = float(row.get("slippage_pct", 0))
                row["price"] = float(row.get("price", 0))
                row["size"] = float(row.get("size", 0))
                trades.append(row)
            except (ValueError, KeyError):
                continue
    return trades

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    trades = load_trades()
    total = len(trades)
    wins = sum(1 for t in trades if t.get("status") == "SUCCESS")
    fails = total - wins
    wr = (wins / total * 100) if total > 0 else 0
    profit = sum(t["profit_usd"] for t in trades if t.get("status") == "SUCCESS")
    best = max([t for t in trades if t.get("status") == "SUCCESS"], key=lambda x: x["profit_usd"]) if wins > 0 else None
    
    cumulative = []
    running = 0.0
    for i, t in enumerate(trades):
        if t.get("status") == "SUCCESS":
            running += t["profit_usd"]
        cumulative.append({"x": i, "timestamp": t.get("timestamp",""), "y": round(running, 6)})
    
    recent = trades[-10:][::-1]
    return jsonify({
        "total_trades": total, "win_count": wins, "fail_count": fails,
        "win_rate": round(wr, 1), "total_profit": round(profit, 4),
        "best_trade_value": round(best["profit_usd"], 6) if best else 0,
        "best_trade_event": best.get("event","") if best else "",
        "cumulative": cumulative, "recent": recent,
    })

def main():
    print(f"Bot Dashboard: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()
