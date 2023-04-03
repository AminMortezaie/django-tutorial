import requests
import os
from dotenv import load_dotenv

load_dotenv()

YOUR_API_KEY = os.getenv("ETH_TRANSACTION_HISTORY_API")


def get_erc20_history(wallet_address):
    responses = []
    tx_hash_map = {}
    get_token_tx_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={YOUR_API_KEY}"
    get_pure_tx_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={YOUR_API_KEY}"
    urls = [get_token_tx_url, get_pure_tx_url]

    c = -1
    for url in urls:
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as err:
            raise "Something went wrong while fetching the URL:" + str(err)
        transactions = response.json()["result"][:15]

        for transaction in transactions:
            c += 1
            # print(c, ":", transaction['hash'])
            sender = transaction['from']
            receiver = transaction['to']
            value = float(transaction['value']) / 10**18
            # print("Sender: ", sender)
            contract_address = ''
            if transaction['contractAddress'] != '':
                contract_address = transaction['contractAddress']
                # print("Contract Address1:", transaction['contractAddress'])

            # Check if the transaction is an ERC-20 token transfer
            if "input" in transaction and len(transaction["input"]) > 2:
                function_signature = transaction["input"][0:10]
                if function_signature == "0xa9059cbb":
                    contract_address = transaction["to"]
                    # Extract the token recipient address and amount from the input data
                    token_recipient = "0x" + transaction["input"][34:74]
                    token_amount = int(transaction["input"][74:], 16) / 10**18
                    # print("Token Transfer:")
                    # print("Contract Address2:", contract_address)
                    receiver = token_recipient
                    value = token_amount

            # print("Receiver: ", receiver)
            # print("Amount: ", value)
            # print("------------------")

            if wallet_address.lower() == str(sender) and transaction['hash'] not in tx_hash_map:
                responses.insert(0,
                                 {"tx": transaction['hash'], "type": "OUT", "amount": value, "contract_address": contract_address})
            elif wallet_address.lower() != str(sender) and transaction['hash'] not in tx_hash_map:
                responses.insert(0,
                                 {"tx": transaction['hash'], "type": "IN", "amount": value, "contract_address": contract_address})
            tx_hash_map[transaction['hash']] = True

    return responses
