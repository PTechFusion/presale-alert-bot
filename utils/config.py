import json
from web3 import Web3, HTTPProvider
import requests

BSC_RPC_URL = "https://go.getblock.io/2533214cb7b74729b4dde72c7be50247"
CONTRACT_ADDRESS = "0x6b3722691e887BA67db49b5FAf1de509c34Dd3FA"
ABI = json.load(open('utils/abi.json','r'))
BOT_TOKEN = "6438227382:AAH-uVGZ42b92g51CogvNxnNIiK4eHWmjxY"
CHAT_ID = -1002242605906
LAUNCH_PRICE = 0.01

last_run = json.load(open('utils/last_run.json', 'r'))

url = "https://api.bscscan.com/api"
parameters = {
    "module": "account",
    "action": "txlist",
    "address": "0x6b3722691e887BA67db49b5FAf1de509c34Dd3FA",
    "startblock": 38291024,
    "endblock": 99999999,
    "page": 1,
    "offset": 10,
    "sort": "asc",
    "apikey": "89ZF4US55QSMHK7ZQ59FHASDIKYBSCZQ9J"
}

parameters['startblock'] = last_run['last_block'] + 1

w3 = Web3(HTTPProvider(BSC_RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=json.dumps(ABI))


def dump_last_run(data):
    json.dump(data, open('utils/last_run.json','w'))
    return True

def get_bnbusd_price():
    resp = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=BNB')
    data = resp.json()
    return float(data['data']['rates']['USDT'])
