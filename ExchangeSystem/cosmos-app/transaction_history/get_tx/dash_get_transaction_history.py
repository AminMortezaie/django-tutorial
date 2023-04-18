import requests
import json
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
getblock_api = os.getenv('GET_BLOCK_API')

# Replace the following variables with your own values
# address = "XtUFSNBRwNrXQjJXMNmM7NFgqX3XFq3xxi"  # the Litecoin address you want to get transactions for


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


def get_transactions_dash(wallet_address):
    responses = []

    # Construct the API URL
    api_url = f"https://dash.getblock.io/{getblock_api}/mainnet/blockbook/api/v2/address/{wallet_address}"

    # Make a GET request to the API URL
    response = requests.get(api_url)

    # print(response.text)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.content)['txids'][:10]
        # print(data)
        print("txs successfully gathered... ")
        # Print out the transactions
        # c =0
        for tx in data:
            tx_hash = tx
            # c += 1
            # print("getting txs details...")
            tx_data = get_tx_data(tx_hash)
            # print(tx_data['hash'])
            # print("this is inputs...")

            for inp in tx_data['vin']:
                sender_address = inp['addresses'][0]
                sender_amount = float(inp['value'])
                if sender_address == wallet_address:
                    responses.insert(0, {"tx": tx_data['txid'], "type": "OUT", "amount": sender_amount})

            # print("this is outputs...")
            for out in tx_data['vout']:
                receiver_address = out['scriptPubKey']['addresses'][0]
                receiver_amount = float(out['value'])

                if receiver_address == wallet_address:
                    responses.insert(0, {"tx": tx_data['txid'], "type": "IN", "amount": receiver_amount})
        return create_response(responses)
    else:
        print(f"Error: {response.status_code}")


def get_tx_data(tx_hash):
    api_url_tx = f"https://dash.getblock.io/{getblock_api}/mainnet/blockbook/api/tx/{tx_hash}"
    response = requests.get(api_url_tx)
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.content)
        # print("this is tx_data...")
        return data
    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"


# res = get_transactions_dash(wallet_address=address)
# print(res)
