import requests

# address = "bnb1tt37jly04qlc6d6njpknl4v72jtz6jtmn8vtd3"


def get_transactions_bep2(wallet_address):
    responses = []
    url = f'https://explorer.binance.org/api/v1/txs?page=1&rows=100&address={wallet_address}'
    result = requests.get(url).json()['txArray']

    for tx in result:
        tx_hash = tx['txHash']
        from_address = tx['fromAddr']
        try:
            to_address = tx['toAddr']
            amount = tx['value']
            contract_address = tx['txAsset']
            if from_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount, "contract_address": contract_address})
            elif to_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount, "contract_address": contract_address})
        except KeyError:
            break

    return responses


# res = get_transactions_bep2(wallet_address=address)
# print(res)
