import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
getblock_api = os.getenv('GET_BLOCK_API')
# address = "one1wx6p8kjucu5llqz79h9pmn0qf55772m2d2xt26"


def get_real_amount(hex_value):
    integer_value = int(hex_value, 16)
    vet_value = integer_value / (10 ** 18)
    return float(vet_value)


def get_transactions_harmony(wallet_address):
    responses = []
    url = 'https://one.getblock.io/mainnet/'
    headers = {'x-api-key': getblock_api, 'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "method": "hmy_getTransactionsHistory",
        "params": [{
            "address": wallet_address,
            "pageIndex": 0,
            "pageSize": 100,
            "fullTx": True,
            "txType": "ALL",
            "order": "DESC"
        }],
        "id": 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()['result']['transactions']
        for tx in result:
            tx_hash = tx['hash']
            sender_address = tx['from']
            receiver_address = tx['to']
            amount = get_real_amount(tx['value'])

            if sender_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
            elif receiver_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})

        return responses
    else:
        print('Error:', response.status_code, response.text)


# res = get_transactions_harmony(wallet_address=address)
# print(res)
