import requests

ACCOUNT_ADDRESS = "0xee226379dB83CfFC681495730c11fDDE79BA4c0C"
api_key = "382d1202-34e8-4b4f-b458-f37df1bff346"
# Replace the ACCOUNT_ADDRESS placeholder with the actual address of the account you want to get the balance for
url = f"https://bsc.getblock.io/api/v1/account/{ACCOUNT_ADDRESS}"


headers = {
    "x-api-key": api_key,
    "accept": "application/json",
    # "content-type": "application/json"
}

response = requests.get(url, headers=headers)
print(response)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Get the balance from the response
    balance = data["balance"]

    print(f"Balance of account {ACCOUNT_ADDRESS}: {balance}")
else:
    print("Failed to get balance")
