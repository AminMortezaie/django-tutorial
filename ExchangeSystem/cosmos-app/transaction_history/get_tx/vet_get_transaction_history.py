import requests
import json

# address = "0x8Fb7C584f37C1CB52D85e52c376442327A401a5A"


def get_real_amount(hex_value):
    integer_value = int(hex_value, 16)
    vet_value = integer_value / (10 ** 18)
    return float(vet_value)


def get_transactions_vet(wallet_address):
    wallet_address = wallet_address.lower()
    responses = []
    # Specify the API endpoint to get transactions for a wallet address
    api_url = 'https://explore-mainnet.veblocks.net/logs/transfer'
    data = {"options": {"offset": 0, "limit": 20}, "criteriaSet": [{"sender": wallet_address}, {"recipient": wallet_address}], "order": "desc"}
    result = requests.post(api_url, data=json.dumps(data)).json()
    for tx in result:
        tx_hash = tx['meta']['txID']
        sender_address = tx['sender']
        receiver_address = tx['recipient']
        amount = get_real_amount(tx['amount'])

        if sender_address == wallet_address:
            responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
        elif receiver_address == wallet_address:
            responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})

    return responses


# res = get_transactions_vet(wallet_address=address)
# print(res)

