import requests
import time
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()
YOUR_API_KEY = os.getenv("BEP20_API")


def get_bep20_history(wallet_address):
    responses = []
    tx_hash_map = {}
    get_token_tx_url = f"https://api.bscscan.com/api?module=account&action=tokentx&address={wallet_address}&startblock=0&endblock=99999999&sort=descc&apikey={YOUR_API_KEY}"
    get_pure_tx_url = f"https://api.bscscan.com/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=descc&apikey={YOUR_API_KEY}"
    urls = [get_token_tx_url, get_pure_tx_url]

    for url in urls:
        retries = 3
        while retries > 0:
            try:
                start_time = time.time()
                response = requests.get(url)
                elapsed_time = time.time() - start_time
                print("Elapsed time: {:.2f} seconds".format(elapsed_time))
                transactions = response.json()["result"][:15]
                for transaction in transactions:
                    timestamp = transaction['timeStamp']
                    sender = transaction['from']
                    receiver = transaction['to']
                    value = float(transaction['value']) / 10**18
                    contract_address = ''
                    if transaction['contractAddress'] != '':
                        contract_address = transaction['contractAddress']

                    # Check if the transaction is an ERC-20 token transfer
                    if "input" in transaction and len(transaction["input"]) > 2:
                        function_signature = transaction["input"][0:10]
                        if function_signature == "0xa9059cbb":
                            contract_address = transaction["to"]
                            # Extract the token recipient address and amount from the input data
                            token_recipient = "0x" + transaction["input"][34:74]
                            token_amount = int(transaction["input"][74:], 16) / 10**18
                            receiver = token_recipient
                            value = token_amount

                    if wallet_address.lower() == str(sender) and transaction['hash'] not in tx_hash_map:
                        responses.insert(0,
                                         {"tx": transaction['hash'], "type": "OUT", "amount": value,
                                          "contract_address": contract_address, "timestamp": str(timestamp)})
                    elif wallet_address.lower() != str(sender) and transaction['hash'] not in tx_hash_map:
                        responses.insert(0,
                                         {"tx": transaction['hash'], "type": "IN", "amount": value,
                                          "contract_address": contract_address, "timestamp": str(timestamp)})
                    tx_hash_map[transaction['hash']] = True
                break
            except Exception as e:
                print(f"Request failed with {type(e).__name__}: {str(e)}")
                retries -= 1
                if retries == 0:
                    print("Max retries exceeded. Giving up.")
                    return []
                else:
                    print(f"Retrying... ({retries} retries left)")
                    sleep(5)

    sorted_data = sorted(responses, key=lambda x: int(x['timestamp']), reverse=False)
    return sorted_data

# Example usage:
# res = get_bsc_history(wallet_address="
