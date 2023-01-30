import requests
import base58
import json

url = "https://trx.getblock.io/wallet/getaccount"
api_key = "YOUR_API-KEY"
tron_address = "TRX6Q82wMqWNbCCiLqejbZe43wk1h1zJHm"
headers = {
    "x-api-key": api_key,
    "accept": "application/json",
    "content-type": "application/json"
}
asset_list = []

'''
gets default public tron address and returns hex
'''


def address_to_hex(address):
    return base58.b58decode(address).hex().upper()[:-8]


def convert_byte_to_json(response):
    json_object = json.loads(response.content)
    return json_object


def get_wallet_balance(json_response):
    for asset in json_response["assetV2"]:
        if asset["value"] > 0:
            correct_value = float(asset["value"] / pow(10, 6))
            asset_list.append({"key": asset["key"], "value": correct_value})


def main():
    payload = {"address": address_to_hex(tron_address)}
    response = requests.post(url, json=payload, headers=headers)
    json_obj = convert_byte_to_json(response)
    get_wallet_balance(json_obj)
    print(asset_list)


main()
