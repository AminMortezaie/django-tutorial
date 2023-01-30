import requests
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Generate a private key from a mnemonic phrase
mnemonic = "YOUR-MEMONIC-CODE"

# Set the recipient address
recipient_address = 'TNo4hakGCPWdPCAejiSENYsDZpccoGF2Xr'
# Set the amount to be transferred
amount = 1
# Set the endpoint URL
endpoint_url = 'https://api.trongrid.io/wallet/easytransfer'

# Set the headers
headers = {
    'Content-Type': 'application/json'
}

private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

# Serialize the private key to a string
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Print the private key as a hexadecimal string
private_key_hex = private_key_bytes.hex()
# Convert the private key to a JSON string
private_key = json.dumps({
    "private_key": private_key_bytes.decode()
})

# Print the JSON string
print("Private Key (JSON):", private_key)

# Set the payload
payload = {
    'privateKey': private_key,
    'toAddress': recipient_address,
    'amount': amount
}

# Send the POST request
response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))

# Print the response
print(response.text)
