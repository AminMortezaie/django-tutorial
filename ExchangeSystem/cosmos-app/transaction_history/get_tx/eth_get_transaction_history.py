import requests

YOUR_API_KEY = 'FBUCR9DE9QPWFN9U83ZKNKZQYDE3VAECSE'
responses = []
tx_hash_map = {}
# wallet_address = "0xac6a04823c043e17de953AcE2F6e6bDb603c78Fb"


def get_erc20_history(wallet_address):
    get_token_tx_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={YOUR_API_KEY}"
    get_pure_tx_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=desc&apikey={YOUR_API_KEY}"
    urls = [get_token_tx_url, get_pure_tx_url]

    try:
        c = 0
        for url in urls:
            response = requests.get(url)
            transactions = response.json()["result"][:15]

            for transaction in transactions:
                c += 1
                print(c, ":", transaction['hash'])
                sender = transaction['from']
                receiver = transaction['to']
                value = float(transaction['value']) / 10**18
                # print("Sender: ", sender)
                contract_address = ''
                if transaction['contractAddress'] != '':
                    contract_address = transaction['contractAddress']
                    print("Contract Address1:", transaction['contractAddress'])

                # Check if the transaction is an ERC-20 token transfer
                if "input" in transaction and len(transaction["input"]) > 2:
                    function_signature = transaction["input"][0:10]
                    if function_signature == "0xa9059cbb":
                        contract_address = transaction["to"]
                        # Extract the token recipient address and amount from the input data
                        token_recipient = "0x" + transaction["input"][34:74]
                        token_amount = int(transaction["input"][74:], 16) / 10**18
                        # print("Token Transfer:")
                        print("Contract Address2:", contract_address)
                        receiver = token_recipient
                        value = token_amount

                print("Receiver: ", receiver)
                print("Amount: ", value)
                print("------------------")

                if wallet_address.lower() == str(sender) and transaction['hash'] not in tx_hash_map:
                    responses.append(
                        {"tx": transaction['hash'], "type": "OUT", "amount": value, "contract_address": contract_address})
                elif wallet_address.lower() != str(sender) and transaction['hash'] not in tx_hash_map:
                    responses.append(
                        {"tx": transaction['hash'], "type": "IN", "amount": value, "contract_address": contract_address})

                tx_hash_map[transaction['hash']] = True

        print(responses)
        return responses
    except:
        return []


# get_erc20_history(wallet_address)