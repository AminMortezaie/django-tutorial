import requests
import json
import base58

api_key = "YOUR-API-KEY"
tron_address = "TRX6Q82wMqWNbCCiLqejbZe43wk1h1zJHm"

'''
As I searched for all of the API, there is no similar endpoint in getblock.io like this.
'''
url = f"https://api.trongrid.io/v1/accounts/{tron_address}/transactions"

headers = {
    "x-api-key": api_key,
    "accept": "application/json",
    "Content-Type": "application/json"
}


def address_to_hex(address):
    return base58.b58decode(address).hex().upper()[:-8]


def main():
    payload = {"address": address_to_hex(tron_address)}
    response = requests.get(url, json=payload, headers=headers)
    json_object = json.loads(response.content)
    pretty = json.dumps(json_object, indent=4)
    print(pretty)


if __name__ == '__main__':
    main()
