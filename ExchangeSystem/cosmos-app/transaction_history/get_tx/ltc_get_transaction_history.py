import requests
import json
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BTC_TRANSACTION_HISTORY_API')

# Replace the following variables with your own values
# address = "LgycvYBU9SVr1dVuq7gC1mdwukyW7qKoeX"  # the Litecoin address you want to get transactions for


def create_response(responses):
    final_response = []
    tx_hash_map = {}
    for res in responses:
        if res["tx"] in tx_hash_map:
            if res["type"] == "IN":
                tx_hash_map[res["tx"]] += res["amount"]
            elif res["type"] == "OUT":
                tx_hash_map[res["tx"]] -= res["amount"]
        else:
            if res["type"] == "IN":
                tx_hash_map[res["tx"]] = res["amount"]
            elif res["type"] == "OUT":
                tx_hash_map[res["tx"]] = -res["amount"]

    for tx in tx_hash_map:
        amount = tx_hash_map[tx]
        if amount > 0:
            final_response.append({"tx": tx, "type": "IN", "amount": amount})
        else:
            final_response.append({"tx": tx, "type": "OUT", "amount": -amount})

    return final_response


def get_transactions_ltc(wallet_address):
    responses = []

    # Construct the API URL
    api_url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{wallet_address}/full?token={api_key}"

    # Make a GET request to the API URL
    response = requests.get(api_url)

    # print(response.text)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.content)
        print("txs successfully gathered... ")
        # Print out the transactions
        for tx in data['txs']:
            tx_hash = tx['hash']
            tx_data = get_tx_data(tx_hash)
            # print(tx_data['hash'])
            # print("this is inputs...")

            for inp in tx_data['inputs']:
                sender_address = inp['addresses'][0]
                sender_amount = float(inp['output_value'])/10**8
                if sender_address == wallet_address:
                    responses.insert(0, {"tx": tx_data['hash'], "type": "OUT", "amount": sender_amount})

            # print("this is outputs...")
            for out in tx_data['outputs']:
                receiver_address = out['addresses'][0]
                receiver_amount = float(out['value'])/10**8

                if receiver_address == wallet_address:
                    responses.insert(0, {"tx": tx_data['hash'], "type": "IN", "amount": receiver_amount})
        return create_response(responses)
    else:
        print(f"Error: {response.status_code}")


def get_tx_data(tx_hash):
    api_url_tx = f"https://api.blockcypher.com/v1/ltc/main/txs/{tx_hash}?instart=0&outstart=0&limit=50"
    response = requests.get(api_url_tx)
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.content)
        # print("this is tx_data...")
        return data
    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"


# res = get_transactions_ltc(wallet_address=address)
# print(res)
