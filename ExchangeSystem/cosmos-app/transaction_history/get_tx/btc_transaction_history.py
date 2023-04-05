import requests


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


def get_transactions_btc(wallet_address):
    responses = []
    api_endpoint = f"https://blockstream.info/api/address/{wallet_address}/txs"
    response = requests.get(api_endpoint)

    if response.status_code == 200:
        transactions = response.json()[:10]
        for tx in transactions:
            tx_hash = tx['txid']
            for inp in tx['vin']:
                sender_address = inp['prevout']['scriptpubkey_address']
                amount = float(inp['prevout']['value'])/10**8
                if sender_address == wallet_address:
                    responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount})
            for out in tx['vout']:
                receiver_address = out['scriptpubkey_address']
                amount = float(out['value'])/10**8
                if receiver_address == wallet_address:
                    responses.insert(0, {"tx":tx_hash, "type": "IN", "amount": amount})
        return create_response(responses)
    else:
        print("Error: Unable to retrieve transactions.")

