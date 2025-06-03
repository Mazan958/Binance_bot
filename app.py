from flask import Flask, request, jsonify
import hmac, hashlib
from binance.client import Client
import os

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
PASSPHRASE = os.environ.get('WEBHOOK_PASSPHRASE')

client = Client(API_KEY, API_SECRET)

@app.route('/')
def home():
    return 'Binance Trading Bot Active ✅'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data['passphrase'] != PASSPHRASE:
        return jsonify({'code': 403, 'msg': 'Wrong passphrase'}), 403

    symbol = data['symbol']
    side = data['side'].upper()

    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=data['quantity']
        )
        return jsonify({'code': 200, 'msg': 'Order placed', 'order': order}), 200

    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
