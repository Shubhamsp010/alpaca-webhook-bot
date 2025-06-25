from flask import Flask, request, jsonify
from alpaca_trade_api.rest import REST
import os

app = Flask(__name__)

# ✅ Use the exact env vars Alpaca expects
ALPACA_API_KEY = os.environ.get("APCA_API_KEY_ID")
ALPACA_SECRET = os.environ.get("APCA_API_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca client
api = REST(ALPACA_API_KEY, ALPACA_SECRET, BASE_URL)

@app.route('/')
def index():
    return "✅ Alpaca Webhook Bot is Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    try:
        symbol = data.get("symbol")
        action = data.get("action")
        price = float(data.get("price"))
        tp = float(data.get("tp"))
        sl = float(data.get("sl"))

        side = "buy" if action == "buy" else "sell"
        qty = 1

        stop_loss = price - sl if side == "buy" else price + sl
        take_profit = price + tp if side == "buy" else price - tp

        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force="gtc",
            order_class="bracket",
            stop_loss={"stop_price": round(stop_loss, 2)},
            take_profit={"limit_price": round(take_profit, 2)}
        )

        return jsonify({"status": "✅ Order sent", "order_id": order.id})
    
    except Exception as e:
        return jsonify({"status": "❌ Error", "message": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
