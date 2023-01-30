import requests
import json
from mnemonic import Mnemonic

api_key = "YOUR-API-KEY"


mnemonic = "YOUR-MEMONIC-CODE"


# Set the recipient address
recipient_address = 'TNo4hakGCPWdPCAejiSENYsDZpccoGF2Xr'

# Set the amount to be transferred
amount = 1

# Set the endpoint URL
endpoint_url = 'https://trx.getblock.io/wallet/easytransfer'

# Set the headers
headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}


# Generate a private key from a mnemonic phrase
def generate_private_key_from_mnemonic(mnemonic):
    # Generate seed
    seed = Mnemonic.to_seed(mnemonic)

    # Create private key from seed
    private_key = seed[:32]
    private_key_hex = private_key.hex()

    # Print the JSON string
    print("Private Key (JSON):", private_key_hex)
    return private_key_hex


# Set the payload
payload = {
    'privateKey': generate_private_key_from_mnemonic(mnemonic),
    'toAddress': recipient_address,
    'amount': amount
}

# Send the POST request
response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
print(response.content)


