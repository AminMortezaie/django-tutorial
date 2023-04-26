import requests
import datetime

# address = "cosmos1g0ffln2weg8wpzpn2hy9t2eddygqcxtvggmyhl"


def get_real_timestamp(date_string):
    date_time = datetime.datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return int(date_time.timestamp())


def get_transactions_cosmos(wallet_address):
    responses = []
    limit = 50
    sender_api_url = f"https://cosmos.lcd.atomscan.com/cosmos/tx/v1beta1/txs?pagination.limit=20&pagination.offset=0&orderBy=ORDER_BY_DESC&events=transfer.sender='{wallet_address}'"
    receiver_api_url = f"https://cosmos.lcd.atomscan.com/cosmos/tx/v1beta1/txs?pagination.limit=20&pagination.offset=0&orderBy=ORDER_BY_DESC&events=transfer.recipient='{wallet_address}'"
    sender_response = requests.get(sender_api_url).json()['tx_responses']
    receiver_response = requests.get(receiver_api_url).json()['tx_responses']

    for tx in sender_response:
        try:
            tx_hash = tx['txhash']
            # sender = tx['tx']['body']['messages'][0]['from_address']
            # receiver = tx['tx']['body']['messages'][0]['to_address']
            amount = float(tx['tx']['body']['messages'][0]['amount'][0]['amount'])/10**6
            timestamp = get_real_timestamp(tx['timestamp'])
            responses.insert(0, {"tx": tx_hash, "type": "OUT", "amount": amount, "timestamp": timestamp})
        except Exception as e:
            pass

    for tx in receiver_response:
        try:
            tx_hash = tx['txhash']
            # sender = tx['tx']['body']['messages'][0]['from_address']
            # receiver = tx['tx']['body']['messages'][0]['to_address']
            amount = float(tx['tx']['body']['messages'][0]['amount'][0]['amount'])/10**6
            timestamp = get_real_timestamp(tx['timestamp'])
            responses.insert(0, {"tx": tx_hash, "type": "IN", "amount": amount, "timestamp": timestamp})
        except Exception as e:
            pass
    sorted_data = sorted(responses, key=lambda x: int(x['timestamp']), reverse=False)
    return sorted_data


# res = get_transactions_cosmos(address)
# print(res)

