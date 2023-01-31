import requests
import json

payload = {
    "address": "41D1CA2403943B8871EC559B6684EEA0B560EEE71B"
}


def trc20_balance(address):
    coins_balance = []
    coins_import = {}
    headers = {"x-api-key": "382d1202-34e8-4b4f-b458-f37df1bff346"}
    uu = f'https://apilist.tronscan.org/api/account?address={address}'
    # uu = f"https://trx.getblock.io/mainnet/wallet/getaccount"
    # result = requests.post(uu, headers=headers, data=json.dumps(payload)).json()
    result = requests.post(uu).json()
    print(result)
    frozen = int(result['totalFrozen'])

    for items in result['tokens']:
        if items['tokenAbbr'] == 'trx' or items['tokenAbbr'] == 'USDC' or \
                items['tokenAbbr'] == 'USDT' or items[
            'tokenAbbr'] == 'JST' or items['tokenAbbr'] == 'SUN' or \
                items['tokenAbbr'] == 'WIN' or items['tokenAbbr'] == 'BTT':
            if items['tokenAbbr'] == 'trx':
                amount = int(items['balance'])
                decimal_amount = int(items['tokenDecimal'])
                frozen = float(frozen / pow(10, decimal_amount))
                ramm = float(amount / pow(10, decimal_amount))
                ramm = ramm + frozen
                coins_import[items['tokenAbbr'].upper()] = ramm

            elif items['tokenAbbr'] == 'BTT':
                amm = int(items['balance'])
                deci = int(items['tokenDecimal'])
                ramm = float(amm / pow(10, deci))
                coins_import['BTT'] = ramm

            else:
                amm = int(items['balance'])
                decimal_amount = int(items['tokenDecimal'])
                ramm = float(amm / pow(10, decimal_amount))
                coins_import[items['tokenAbbr'].upper()] = ramm

    coins_import['address'] = address

    coins_balance.append(coins_import)

    print(coins_balance)


trc20_balance("TRsf7fjqaGJWej3i8rFZHRm8XGY2nb6SbG")
