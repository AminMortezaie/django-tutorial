import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BLOCK_FROST_MAINNET_FIRST_API")

# Set the Cardano API endpoint
url = "https://cardano-mainnet.blockfrost.io/api/v0"

# Set the Cardano account for which you want to retrieve transaction history
# address = "addr1v8tkdh5rnc254xzrzt7zgwkyu3545vn995zfx4rhn0mvzuqm4a59d"


# Set the request headers with your API key
headers = {"project_id": api_key}


def get_cardano_history(wallet_address):
    responses = []
    # Send a GET request to the Cardano API with the address as a parameter to retrieve the transaction history
    response = requests.get(f"{url}/addresses/{wallet_address}/transactions", headers=headers)
    if response.status_code == 200:
        transactions = response.json()
        for tx in transactions:
            tx_hash = tx["tx_hash"]
            tx_response = requests.get(f"{url}/txs/{tx_hash}/utxos", headers=headers)
            # print(tx_response.text)
            if tx_response.status_code == 200:
                tx_data = tx_response.json()

                sender = tx_data["inputs"][0]["address"]
                receiver = tx_data["outputs"][0]["address"]
                amount = float(tx_data["outputs"][0]["amount"][0]["quantity"])/10**6

                if sender == wallet_address:
                    responses.append({"tx": tx_hash, "type": "OUT", "amount": amount})
                else:
                    responses.append({"tx": tx_hash, "type": "IN", "amount": amount})
            else:
                print(f"Error retrieving transaction data for transaction hash {tx_hash}. Response code: {tx_response.status_code}")

        return responses
    else:
        print(f"Error retrieving transaction history. Response code: {response.status_code}")
        return responses


# print(get_cardano_history(wallet_address=address))