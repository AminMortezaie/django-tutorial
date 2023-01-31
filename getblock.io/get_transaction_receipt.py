import requests
import json

api_key = "382d1202-34e8-4b4f-b458-f37df1bff346"
transaction_id = "1d1fa771b91b65341db116519bf2bf217c32341f9c01026be6ff6723d32f4ade"

url = "https://trx.getblock.io/mainnet/fullnode/jsonrpc"

header = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}
payload = {
    "jsonrpc": "2.0",
    "method": "eth_getTransactionReceipt",
    "params": [
        transaction_id
    ],
    "id": "getblock.io"
}

response = requests.post(url, headers=header, data=json.dumps(payload))
json_object = json.loads(response.content)

print(json_object["result"])
