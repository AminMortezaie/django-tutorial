from celery import shared_task
from .models import Wallet, Coin, Network, TransactionHistory
from django.core.cache import cache
from .get_tx import btc_transaction_history, eth_get_transaction_history, \
    trc20_get_transaction_history, cardano_get_transaction_history, ltc_get_transaction_history,\
    bch_get_transaction_history, bsc_get_transaction_history
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

        if wallet_network == 'btc':
            print("wallet_network is btc")
            network = Network.objects.filter(name='btc').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            coin = Coin.objects.filter(symbol='BTC', network=network).first()
            latest_txs = btc_transaction_history.get_transactions_btc(wallet_address)

        elif wallet_network == 'litecoin':
            print("wallet_network is litecoin")
            network = Network.objects.filter(name='litecoin').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            coin = Coin.objects.filter(symbol='LTC', network=network).first()
            latest_txs = ltc_get_transaction_history.get_transactions_ltc(wallet_address)

        elif wallet_network == 'bch':
            print("wallet_network is bch")
            network = Network.objects.filter(name='bch').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            coin = Coin.objects.filter(symbol='BCH', network=network).first()
            latest_txs = bch_get_transaction_history.get_transactions_bch(wallet_address)

        elif wallet_network == 'cardano':
            print("wallet_network is cardano")
            network = Network.objects.filter(name='cardano').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            coin = Coin.objects.filter(symbol='ADA', network=network).first()
            latest_txs = cardano_get_transaction_history.get_cardano_history(wallet_address)

        elif wallet_network == 'erc20':
            print("wallet_network is erc20")
            network = Network.objects.filter(name='erc20').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            latest_txs = eth_get_transaction_history.get_erc20_history(wallet_address)

        elif wallet_network == 'bsc':
            print("wallet_network is bsc")
            network = Network.objects.filter(name='bsc').first()
            wallet = Wallet.objects.filter(address=wallet_address).first()
            latest_txs = bsc_get_transaction_history.get_bsc_history(wallet_address)

        elif wallet_network == 'trc20':
            print("wallet network is trc20")
            network = Network.objects.filter(name='trc20').first()
            print(wallet_address)
            wallet = Wallet.objects.filter(address=wallet_address).first()
            latest_txs = trc20_get_transaction_history.get_trc20_transactions(wallet_address)

        else:
            latest_txs = None

        # Iterate through the transactions and update your database
        if latest_txs is not None:
            for tx in latest_txs:
                print("getting transactions for ")
                if (wallet_network == 'erc20' or wallet_network == 'trc20' or wallet_network == 'bsc') and tx['contract_address'] != '':
                    coin = Coin.objects.filter(contract=tx['contract_address'], network=network).first()
                    if coin is None:
                        coin = Coin.objects.filter(symbol='no symbol', network=network).first()

                elif wallet_network == 'erc20' and tx['contract_address'] == '':
                    coin = Coin.objects.filter(symbol='ETH', network=network).first()

                elif wallet_network == 'bsc' and tx['contract_address'] == '':
                    coin = Coin.objects.filter(symbol='BNB', network=network).first()

                elif wallet_network == 'trc20' and tx['contract_address'] == '':
                    coin = Coin.objects.filter(symbol='TRX', network=network).first()

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
                    tx_obj.save()
                    print("tx might be saved...")
                else:
                    print("Transaction already exists in database")

                # Invalidate the cached result for this wallet so that it will be refreshed on the next request
                cache.delete(f'transactions_{wallet_id}')
        else:
            print("no transaction received.")
