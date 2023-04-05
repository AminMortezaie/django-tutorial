import requests

address = "bc1qe0rfrt8yajnfys7786jyg6d3lsw6xzj332k05p"

test_res = [{'tx': 'b18795e9351485eb3f91d73050a99dc8c90b35b1faac2870c892511ddcc20b15', 'type': 'OUT', 'amount': 0.00979236}, {'tx': 'a63ae816c3031275d058705aec7dd17318635aa444efaea6a052384a62a3fcea', 'type': 'IN', 'amount': 0.00978381}, {'tx': '047f91d8e30b84675e58a0389012aaf6935f00ad80e773ad83445171fdfa1fbf', 'type': 'IN', 'amount': 0.0136396}, {'tx': 'e96c355426d44d1e771cd77a996bae2a633c6827ad96610fba9bf79ef26e343a', 'type': 'OUT', 'amount': 0.0136396}, {'tx': 'e96c355426d44d1e771cd77a996bae2a633c6827ad96610fba9bf79ef26e343a', 'type': 'OUT', 'amount': 0.00978381}, {'tx': '96f35857c35f9034e8bf3149da32fb4225eb4ddd3dd29dabfa36b67e9fbf35dd', 'type': 'IN', 'amount': 0.0096917}, {'tx': '3eb25ca2417f90c5c063ba8b95ebc870cde511d1dc22d01c4f182210207b52f8', 'type': 'OUT', 'amount': 0.0096917}, {'tx': '40647e01f334c35365195971b858024ffa7c450b4f57636805548ad1137cee2e', 'type': 'IN', 'amount': 0.00942438}, {'tx': 'df04330a9ae4454e058c9447ae871efda9216c8260664eb855c2e8ff37ea0bba', 'type': 'OUT', 'amount': 0.00942438}, {'tx': 'd68bedbdf607da073edd77218f4c1af43b684f79683ba82516a25e14877aa06b', 'type': 'IN', 'amount': 0.00975913}, {'tx': '286891cba7741324db39e7978b13f88b0c4975eeb981a7fdca7606df60d49b5b', 'type': 'OUT', 'amount': 0.00975913}]


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

