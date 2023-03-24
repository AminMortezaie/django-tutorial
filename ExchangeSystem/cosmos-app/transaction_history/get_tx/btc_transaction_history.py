import blockcypher
import requests
import json

api_key = "27f383ae4ce240f897307c705b22f195"
# Set the API endpoint URL


# Make an HTTP GET request to the endpoint and store the response in 'response'

responses = []


# Print out some details for each transaction in the array
def get_transactions_btc(wallet_address):
    url = f'https://api.blockcypher.com/v1/btc/main/addrs/{wallet_address}/full?token={api_key}'
    response = requests.get(url)
    # Convert the JSON response to a Python dictionary
    data = json.loads(response.content)

    # Extract the transactions array from the dictionary
    transactions = data['txs']
    for tx in transactions:
        # print('Sender addresses and amounts:')
        for i in range(len(tx['inputs'])):
            if tx['inputs'][i]['addresses'][0] == wallet_address:
                # print(tx['inputs'][i]['addresses'], tx['inputs'][i]['output_value'] / 100000000)
                responses.insert(1, {"tx": tx['hash'], "type": "OUT", "amount": tx['inputs'][i]['output_value'] / 100000000})
                # print(response)

        # Loop through each output address (receiver) and print it, along with the amount received
        # print('Receiver addresses and amounts:')
        for i in range(len(tx['outputs'])):
            if tx['outputs'][i]['addresses'][0] == wallet_address:
                # print(tx['outputs'][i]['addresses'], tx['outputs'][i]['value'] / 100000000)
                responses.insert(1, {"tx": tx['hash'], "type": "IN", "amount": tx['outputs'][i]['value'] / 100000000})
                # print(response)

    # print(response)
    return responses

