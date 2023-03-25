from celery import shared_task
from .models import Wallet, Coin, Network, TransactionHistory
from django.core.cache import cache
from .get_tx import btc_transaction_history, eth_get_transaction_history
from datetime import datetime, timedelta


@shared_task(name="update_transactions")
def update_transactions():
    time_threshold = datetime.now() - timedelta(seconds=60)
    print("updating...")
    # Get all wallets from the database
    wallets = Wallet.objects.all()

    # Loop through each wallet and retrieve the latest transactions
    for wallet in wallets:
        wallet_id = wallet.id
        wallet_network = str(wallet.network)
        wallet_address = str(wallet.address)
        print("wallet_network:", wallet_network)
        print("wallet_address:", wallet_address)
        if wallet_network == 'btc':
            print("wallet_network is btc")
            network = Network.objects.filter(name='btc').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            coin = Coin.objects.filter(symbol='BTC', network=network).first()
            latest_txs = btc_transaction_history.get_transactions_btc(wallet_address)
            print("btc network txs:")
            # print(latest_txs)
        elif wallet_network == 'erc20':
            print("wallet_network is erc20")
            network = Network.objects.filter(name='erc20').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            latest_txs = eth_get_transaction_history.get_erc20_history(wallet_address)
            print("erc20 network txs:")
            # print(latest_txs)

        else:
            latest_txs = {}

        # Iterate through the transactions and update your database
        for tx in latest_txs:
            print("getting transactions...")
            if wallet_network == 'erc20' and tx['contract_address'] != '':
                coin = Coin.objects.filter(contract=tx['contract_address'], network=network).first()
                if coin is None:
                    # print(network)
                    coin = Coin.objects.filter(symbol='no symbol', network=network).first()
                    # print(coin)

            elif wallet_network == 'erc20' and tx['contract_address'] == '':
                coin = Coin.objects.filter(symbol='ETH', network=network).first()

            existing_tx = TransactionHistory.objects.filter(transaction_hash=tx['tx'], transaction_type=tx['type'], amount=tx['amount'], wallet=wallet).first()

            if not existing_tx:
                # Convert the transaction data to a dictionary compatible with the TransactionHistory model
                tx_data = {
                    'transaction_hash': tx['tx'],
                    'amount': tx['amount'],
                    'transaction_type': tx['type'],
                    'network': network,
                    'wallet': wallet,
                    'coin': coin
                }
                # Create a new TransactionHistory object

                tx_obj = TransactionHistory(**tx_data)
                print(tx_obj)
                tx_obj.save()
                print("tx might be saved...")
            else:
                print("Transaction already exists in database")

        # Invalidate the cached result for this wallet so that it will be refreshed on the next request
        cache.delete(f'transactions_{wallet_id}')