import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("POLKADOT_API")

# address = "166xo4EcBeToC4j3t3xCpCP5RqBk2N4AyWRvBGHDaP3sbXk5"


def get_transactions_polkadot(wallet_address):
    responses = []
    api_url = 'https://polkadot.api.subscan.io/api/scan/transfers'
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    data = {
        "row": 100,
        "page": 0,
        "address": wallet_address
    }
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data)).json()['data']['transfers']

        for tx in response:
            tx_hash = tx['hash']
            from_address = tx['from']
            to_address = tx['to']
            amount = tx['amount']
            if from_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
            elif to_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})
        return responses

    except Exception as e:
        print(f"Request failed with {type(e).__name__}: {str(e)}")
        return responses


# res = get_transactions_polkadot(wallet_address=address)
# print(res)
