import kraken_requests
import requests
import rsi_calculator
from IPython import embed

COINS = [
    {"pair": 'XXBTZUSD', "asset": 'XXBT'},
    {"pair": 'XETHZUSD', "asset": 'XETH'},
    {"pair": 'XLTCZUSD', "asset": 'XLTC'},
    {"pair": 'ADAUSD', "asset": 'ADA'},
    {"pair": 'DOTUSD', "asset": 'DOT'},
    {"pair": 'BCHUSD', "asset": 'BCH'},
    {"pair": 'XXLMZUSD', "asset": 'XXLM'},
    {"pair": 'XDGUSD', "asset": 'XXDG'},
    {"pair": 'XXMRZUSD', "asset": 'XXMR'},
    {"pair": "KEEPUSD", "asset": "KEEP"},
    {"pair": "ATOMUSD", "asset": "ATOM"}
]

def main():
    orders = {
        "buy": [],
        "sell": []
    }
    for coin in COINS:
        ohlc_data = kraken_requests.get_ohlc_data(coin["pair"])
        rsi = rsi_calculator.calc(ohlc_data)
        if rsi < 40:
            orders["buy"].append(coin)
        elif rsi > 55:
            orders["sell"].append(coin)

    current_holdings = kraken_requests.get_current_holdings()
    for coin in orders['buy']:
        purchase_volume = kraken_requests.calcualte_purchase_volume(coin["pair"])
        if coin['asset'] not in current_holdings or float(current_holdings[coin["asset"]]) < purchase_volume / 2:
            kraken_requests.buy_pair(coin["pair"], purchase_volume)
    
    for coin in orders['sell']:
        if coin['asset'] in current_holdings and coin['asset'] and float(current_holdings[coin['asset']]) > 0.0:
            kraken_requests.sell_pair(coin["pair"], current_holdings[coin["asset"]])

if __name__ == "__main__":
    main()
