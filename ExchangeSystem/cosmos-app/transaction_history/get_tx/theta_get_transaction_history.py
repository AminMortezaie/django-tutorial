import requests

# address = "0xf51Ec90C76cD5A05D689F5f961F5F76727576AED"


def get_transactions_theta(wallet_address):
    wallet_address = wallet_address.lower()
    responses = []
    api_url = f'http://www.thetascan.io/api/transactions/?address={wallet_address}'
    try:
        response = requests.get(api_url).json()
        # print(response)

        for tx in response:
            # print(tx)
            tx_hash = tx['hash']
            from_address = tx['sending_address']
            to_address = tx['recieving_address']
            amount = tx['theta']
            if from_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
            elif to_address == wallet_address:
                responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})
        return responses

    except Exception as e:
        print(f"Request failed with {type(e).__name__}: {str(e)}")
        return responses


# res = get_transactions_theta(wallet_address=address)
# print(res)
