import requests
import json
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BTC_TRANSACTION_HISTORY_API')

# Replace the following variables with your own values
address = "LgycvYBU9SVr1dVuq7gC1mdwukyW7qKoeX"  # the Litecoin address you want to get transactions for

test_res = [{'tx': '308cf9cf5c765188e1db35ca05306d2cfc8a62dbfc31d061c1c1027e223163dc', 'type': 'IN', 'amount': 101.56485298}, {'tx': '308cf9cf5c765188e1db35ca05306d2cfc8a62dbfc31d061c1c1027e223163dc', 'type': 'OUT', 'amount': 101.77596548}, {'tx': 'f5a51dcb1d24e642cd9216364210ec69c8fa71ea6a0ef6d95e691b3643621b4a', 'type': 'IN', 'amount': 54.36649336}, {'tx': 'f5a51dcb1d24e642cd9216364210ec69c8fa71ea6a0ef6d95e691b3643621b4a', 'type': 'OUT', 'amount': 64.36660586}, {'tx': '37e70fff3a2f8fedd6579e893baf0cd1a4bfa7e3196c8524edbf9f3e1b1c60e7', 'type': 'IN', 'amount': 54.13346571}, {'tx': '37e70fff3a2f8fedd6579e893baf0cd1a4bfa7e3196c8524edbf9f3e1b1c60e7', 'type': 'OUT', 'amount': 54.36649336}, {'tx': '31e05ab9dc91d99acfa2ae9205d48b6467420ad2713304eaa6f35fd077516acd', 'type': 'IN', 'amount': 51.85944198}, {'tx': '31e05ab9dc91d99acfa2ae9205d48b6467420ad2713304eaa6f35fd077516acd', 'type': 'OUT', 'amount': 54.13346571}, {'tx': '80a94aa5f22263007eadf66b1b5903ead6e832fce77015513196b1764ca915d3', 'type': 'IN', 'amount': 51.64349548}, {'tx': '80a94aa5f22263007eadf66b1b5903ead6e832fce77015513196b1764ca915d3', 'type': 'OUT', 'amount': 51.85944198}, {'tx': 'cafe1de4137fbb4ff9e6efae2b330678ea0f52dec40d59bea1074bd220a58e35', 'type': 'IN', 'amount': 51.39938298}, {'tx': 'cafe1de4137fbb4ff9e6efae2b330678ea0f52dec40d59bea1074bd220a58e35', 'type': 'OUT', 'amount': 51.64349548}, {'tx': '03f0d6882a85165081200fdc3fcd6665bb4cd38a0914aea0c90bd48fc9dedd69', 'type': 'IN', 'amount': 51.19527048}, {'tx': '03f0d6882a85165081200fdc3fcd6665bb4cd38a0914aea0c90bd48fc9dedd69', 'type': 'OUT', 'amount': 51.39938298}, {'tx': '1d0c7aac5dc95404905c64ededf27dbedbb0c345b59011fcfbfda797b12f3fc7', 'type': 'IN', 'amount': 50.98715798}, {'tx': '1d0c7aac5dc95404905c64ededf27dbedbb0c345b59011fcfbfda797b12f3fc7', 'type': 'OUT', 'amount': 51.19527048}, {'tx': '7fd8df7be27ddd0a2bb43c7e635c475774852b0abdad4ad217897e240af5bff6', 'type': 'IN', 'amount': 242.34575771}, {'tx': '1673ba2f6ff1aa24bf19e1e02d8026646f623e747842c7ac296781160ef3965f', 'type': 'IN', 'amount': 20.98704548}, {'tx': '1673ba2f6ff1aa24bf19e1e02d8026646f623e747842c7ac296781160ef3965f', 'type': 'OUT', 'amount': 50.98715798}]


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


def get_txs(wallet_address):
    responses = []
    txs_hash_map = {}

    # Construct the API URL
    api_url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/full?token={api_key}"

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
    api_url_tx = f"https://api.blockcypher.com/v1/ltc/main/txs/{tx_hash}?limit=50?token={api_key}"
    response = requests.get(api_url_tx)
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.content)
        # print("this is tx_data...")
        return data
    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"


res = get_txs(wallet_address=address)
print(res)



