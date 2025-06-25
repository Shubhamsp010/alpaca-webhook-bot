from flask import Flask, request, jsonify
from alpaca_trade_api.rest import REST

app = Flask(__name__)

# Replace with your actual keys
ALPACA_API_KEY = "PKCZI5K3MYNFHLEECMYV"
ALPACA_SECRET = "eYbOLgICD5I3XMsDw4XVY7noVZg24sAnc91UOmH3"
BASE_URL = "https://paper-api.alpaca.markets/v2"

api = REST(ALPACA_API_KEY, ALPACA_SECRET, BASE_URL)

@app.route('/')
def index():
    return 'Alpaca Webhook Bot is Running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    action = data.get("action")
    price = float(data.get("price"))
    tp = float(data.get("tp"))
    sl = float(data.get("sl"))

    qty = 1  # You can make this dynamic

    side = "buy" if action == "buy" else "sell"
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

    return jsonify({"status": "order sent", "order_id": order.id})
