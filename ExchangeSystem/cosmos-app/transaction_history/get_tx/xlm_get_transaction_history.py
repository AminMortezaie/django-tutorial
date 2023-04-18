import requests

# address = "GCORXHCLQ256IPQCWD3RCJXKPYD6BECF2TUKDRRMN6XR6UXP3XK7DYWU"


def get_transactions_xlm(wallet_address):
    responses = []
    api_url = f'https://horizon.stellar.org/accounts/{wallet_address}/payments?cursor=&limit=10&order=desc'
    response = requests.get(api_url).json()['_embedded']['records']
    for tx in response:
        # print(tx)
        tx_hash = tx['transaction_hash']
        from_address = tx['from']
        to_address = tx['to']
        amount = tx['amount']
        if from_address == wallet_address:
            responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
        elif to_address == wallet_address:
            responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})
    return responses


# get_transactions_xlm(wallet_address=address)
