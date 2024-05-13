import requests
import time
from utils.config import *
from utils.bot import send_presale_alert


def get_event():
    # global parameters
    while True:
        time.sleep(2)
        response = requests.get(url, params=parameters)      
        if response.status_code == 200:
            data = response.json()
            transactions = data['result']
            
            for transaction in transactions:
                alert= False
                if transaction['functionName'] == 'buyToken()':
                    bnbusd = get_bnbusd_price()
                    
                    print("Found a transaction with functionName 'buyToken()':")
                    bought_with = Web3.from_wei(int(transaction['value']), 'ether')
                    print(f"The value of the transaction is {bought_with} BNB")
                    result = contract.functions.getpriceAndStage().call()
                    tokens = float(bnbusd) * int(transaction['value'])/int(result[0])
                    print(f'Tokens: {tokens} | Stage: {result[1]}')
                    unit = "BNB"
                    alert = True
                    
                elif "buyTokenUSDT" in transaction['functionName']:
                    result = contract.functions.getpriceAndStage().call()
                    data = transaction['input'].replace('0xb5e75e1c','')
                    bought_with = int(data, 16)/10**18
                    tokens = bought_with * 77580
                    unit = "USDT"
                    alert = True
                elif "buyTokenUSDC" in transaction['functionName']:
                    result = contract.functions.getpriceAndStage().call()
                    data = transaction['input'].replace('0x317d71a5','')
                    bought_with = int(data, 16)/10**18
                    tokens = bought_with * 77580
                    unit = "USDC"
                    alert = True
                    # print(transaction)
                if alert:
                    send_presale_alert({'tx': transaction, 'stage': result[1], 'stage_price': Web3.from_wei(int(result[0]),'ether'), 'tokens': tokens, 'amountIn': bought_with,'unit':unit})
                
            parameters["startblock"] = int(transaction['blockNumber']) + 1
            last_run['last_block'] = parameters["startblock"]
            dump_last_run(last_run)
                    
        else:
            print("Error:", response.status_code, response.text)

get_event()