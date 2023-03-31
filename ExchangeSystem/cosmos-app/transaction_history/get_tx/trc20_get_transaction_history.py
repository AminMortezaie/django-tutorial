import os

import requests
import base58
from dotenv import load_dotenv

load_dotenv()
# Replace YOUR_API_KEY with your TronGrid API key
api_key = os.getenv("TRON_GRID_API")

# Replace WALLET_ADDRESS with the address of the TRX wallet you want to query
# wallet_address = "TTmaAAbFPtACn1amP3FBkmmUygFh8udAvA"
responses = []
tx_hash_map = {}


def check_for_address(wallet_address):
    decoded_bytes = base58.b58decode(wallet_address)
    hex_str = decoded_bytes.hex()
    return hex_str[:-8]


def get_trc20_transactions(wallet_address):
    get_token_tx_url = f"https://api.trongrid.io/v1/accounts/{wallet_address}/transactions/trc20"
    get_pure_tx_url = f"https://api.trongrid.io/v1/accounts/{wallet_address}/transactions"

    urls = [get_token_tx_url, get_pure_tx_url]
    for url in urls:
        response = requests.get(url,
                                headers={"TRON-PRO-API-KEY": api_key})

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_response = response.json()

            # Extract the transaction data from the response
            transactions = json_response["data"]

            # Print the transaction data
            for transaction in transactions:
                # noinspection PyBroadException
                try:
                    if transaction['transaction_id']:
                        if transaction['from'] == wallet_address:
                            tx_type = "OUT"
                        else:
                            tx_type = "IN"
                        responses.append({"tx": str(transaction['transaction_id']),
                                          "type": tx_type, "amount": str(int(transaction['value']) / 10 ** 6),
                                          "contract_address": str(transaction['token_info']['address']),
                                          "timestamp": str(transaction['block_timestamp'])})
                        tx_hash_map[transaction['transaction_id']] = True
                except:
                    if transaction['txID'] and transaction['txID'] not in tx_hash_map:
                        payload = transaction['raw_data']['contract'][0]['parameter']['value']
                        if payload['owner_address'] == check_for_address(wallet_address):
                            tx_type = "OUT"
                        else:
                            tx_type = "IN"
                        responses.append({"tx": str(transaction['txID']),
                                          "type": str(tx_type),
                                          "amount": int(payload['amount']) / 10 ** 6,
                                          "contract_address": "",
                                          "timestamp": str(transaction['raw_data']['timestamp'])})
                        tx_hash_map[transaction['txID']] = True

        else:
            # Handle errors here
            print("Error:", response.text)
    sorted_data = sorted(responses, key=lambda x: int(x['timestamp']), reverse=False)
    print(sorted_data)


# get_trc20_transactions(wallet_address)



