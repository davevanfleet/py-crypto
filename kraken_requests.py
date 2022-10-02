import requests
import os
import time
import urllib.parse
import hashlib
import hmac
import base64
from dotenv import load_dotenv

#########################
# LIBRARY CONFIGURATION #
#########################

load_dotenv()

api_sec = os.environ.get("KRAKEN_API_SEC_KEY")
api_key = os.environ.get("KRAKEN_API_PUB_KEY")
api_url = "https://api.kraken.com"

DEFAULT_PURCHASE_USD = 30.00

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

####################
# PUBLIC ENDPOINTS #
####################

def get_ohlc_data(pair):
    res = requests.get(f'{api_url}/0/public/OHLC?interval=1440&pair={pair}')
    body = res.json()
    return body['result'][pair]

def calcualte_purchase_volume(pair):
    res = requests.get(f'{api_url}/0/public/Trades?pair={pair}')
    body = res.json()
    last_trade = float(body['result'][pair][-1][0])
    return DEFAULT_PURCHASE_USD / last_trade

def calcualte_current_value(pair, holding):
    res = requests.get(f'{api_url}/0/public/Trades?pair={pair}')
    body = res.json()
    last_trade = float(body['result'][pair][-1][0])
    return last_trade * float(holding)

#####################
# PRIVATE ENDPOINTS #
#####################

def get_current_holdings():
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)
    body = resp.json()
    return body['result']

def buy_pair(pair, volume):
    print(f'buy {volume} {pair}')
    resp = kraken_request('/0/private/AddOrder', {
        "nonce": str(int(1000*time.time())),
        "ordertype": "market",
        "type": "buy",
        "volume": volume,
        "pair": pair
    }, api_key, api_sec)
    body = resp.json()
    return body['result']

def sell_pair(pair, volume):
    print(f'sell {volume} {pair}')
    resp = kraken_request('/0/private/AddOrder', {
        "nonce": str(int(1000*time.time())),
        "ordertype": "market",
        "type": "sell",
        "volume": volume,
        "pair": pair
    }, api_key, api_sec)
    body = resp.json()
    return body['result']
