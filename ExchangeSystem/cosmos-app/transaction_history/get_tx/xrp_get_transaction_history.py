import requests

# address = "rHttapRsfyi1F269p4ozV58N6MmDTTSgwB"


def get_transactions_xrp(wallet_address):
    responses = []
    api_url = f'https://api.xrpscan.com/api/v1/account/{wallet_address}/transactions'

    try:
        result = requests.get(api_url).json()['transactions']
    except requests.exceptions.ConnectionError as e:
        print(f"Request failed with {type(e).__name__}: {str(e)}")
        return responses

    for tx in result:
        from_address = tx['Account']
        to_address = tx['Destination']
        amount = float(tx['Amount']['value'])/10**6
        coin = tx['Amount']['currency']
        tx_hash = tx['hash']
        tx_result = (tx['meta']['TransactionResult'] == 'tesSUCCESS')

        if from_address == wallet_address and coin == "XRP" and tx_result:
            responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
        elif to_address == wallet_address and coin == "XRP" and tx_result:
            responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})

    return responses


# res = get_transactions_xrp(wallet_address=address)
# print(res)
