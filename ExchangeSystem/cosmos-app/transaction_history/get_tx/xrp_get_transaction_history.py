import requests

# address = "rh4mXbGzMho3Vxwf8uwpHjBxZfkhnMZusS"


def get_transactions_xrp(wallet_address):
    responses = []
    api_url = f'https://api.xrpscan.com/api/v1/account/{wallet_address}/transactions'
    result = requests.get(api_url).json()['transactions']

    for tx in result:
        from_address = tx['Account']
        to_address = tx['Destination']
        amount = float(tx['Amount']['value'])/10**6
        coin = tx['Amount']['currency']
        tx_hash = tx['hash']
        if from_address == wallet_address and coin == "XRP":
            responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
        elif to_address == wallet_address:
            responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})

    return responses


# res = get_transactions_xrp(wallet_address=address)
# print(res)
