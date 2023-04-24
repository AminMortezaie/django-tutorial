import requests
import json
from time import sleep

# address = 'DkdT8hzJmXRsJ4tTJLxh9TucQqq5hmo2pHJM3NpXcVaH'
rpc_url = 'https://alien-spring-season.solana-mainnet.discover.quiknode.pro/ae22f1a0a4da3d5e3a570d4e2270f82666b12096/'


def get_transactions_solana(wallet_address):
    responses = []
    limit = 50
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": [wallet_address, {"limit": limit}]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(rpc_url, data=json.dumps(payload), headers=headers)
    result = response.json()['result']
    print("txs successfully gathered...")
    for tx in result:
        tx_hash = tx['signature']
        try:
            if get_tx_data(tx_hash, wallet_address) is not None:
                responses.insert(0, get_tx_data(tx_hash, wallet_address))
                print("tx added...")
        except Exception as e:
            print(f"Request failed with {type(e).__name__}: Token is not solana.")
    return responses


def get_tx_data(tx_hash, wallet_address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [tx_hash]
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(rpc_url, data=json.dumps(payload), headers=headers)
        result = response.json()['result']
        account_keys = result['transaction']['message']['accountKeys']
        pre_balances = result['meta']['preBalances']
        post_balances = result['meta']['postBalances']

        for number in range(len(account_keys)):
            amount = (float(post_balances[number]) - float(pre_balances[number])) / 10**9
            if account_keys[number] == wallet_address:
                if account_keys[-1] == "11111111111111111111111111111111":
                    if amount > 0:
                        return {"tx": tx_hash, "type": "IN", "amount": amount}
                    else:
                        return {"tx": tx_hash, "type": "OUT", "amount": -amount}

    except Exception as e:
        print(f"Request failed with {type(e).__name__}: {str(e)}")


# res = get_transactions_solana(wallet_address=address)
# print(res)

