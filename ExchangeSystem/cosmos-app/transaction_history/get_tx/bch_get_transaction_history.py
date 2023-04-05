import requests

# address = "qr68aemt96453vvuhzyj827e8uzcqzvvqcvrhczqu6"


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


def get_transactions_bch(wallet_address):
    responses = []
    api_endpoint = f"https://bch-chain.api.btc.com/v3/address/{wallet_address}/tx"
    response = requests.get(api_endpoint)
    # print(response.text)

    if response.status_code == 200:
        transactions = response.json()["data"]["list"]
        for tx in transactions:
            tx_hash = tx['hash']
            for inp in tx['inputs']:
                amount = float(inp['prev_value'])/10**8
                inp_address = inp['prev_addresses'][0]
                sender_address = inp_address.split("bitcoincash:")[1]
                if sender_address == wallet_address:
                    responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})

            for out in tx['outputs']:
                amount = float(out['value']/10**8)
                out_address = out['addresses'][0]
                receiver_address = out_address.split("bitcoincash:")[1]
                if receiver_address == wallet_address:
                    responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount})
        return create_response(responses)
    else:
        print("Error: Unable to retrieve transactions.")


# res = get_transactions_bch(wallet_address=address)
# print(res)