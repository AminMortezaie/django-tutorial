from celery import shared_task, Task
from .models import Wallet, Coin, Network, TransactionHistory
from django.core.cache import cache
from .get_tx import (
    btc_transaction_history,
    eth_get_transaction_history,
    trc20_get_transaction_history,
    cardano_get_transaction_history,
    ltc_get_transaction_history,
    bch_get_transaction_history,
    bep20_get_transaction_history,
    doge_get_transaction_history,
    dash_get_transaction_history,
    bep2_get_transaction_history,
    xrp_get_transaction_history,
    xlm_get_transaction_history,
    polkadot_get_transaction_history,
    theta_get_transaction_history,
    dgb_get_transaction_history,
    zcash_get_transaction_history,
    solana_get_transaction_history,
    vet_get_transaction_history,
    polygon_get_transaction_history,
    harmony_get_transaction_history,
    cosmos_get_transaction_history
)
from datetime import datetime, timedelta
from django.db import transaction


@shared_task(name="update_transactions")
def update_transactions():
    with transaction.atomic():
        lock_id = "update_transactions_lock"
        acquire_lock = lambda: cache.add(lock_id, "true", 60 * 5)
        release_lock = lambda: cache.delete(lock_id)
        if acquire_lock():
            try:
                time_threshold = datetime.now() - timedelta(seconds=60)
                print("updating...")
                # Get all wallets from the database
                wallets = Wallet.objects.all()

                # Loop through each wallet and retrieve the latest transactions
                for wallet in wallets:
                    wallet_id = wallet.id
                    wallet_network = str(wallet.network)
                    wallet_address = str(wallet.address)

                    # if wallet_network == 'btc':
                    #     print("wallet_network is btc")
                    #     network = Network.objects.filter(name='btc').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     coin = Coin.objects.filter(symbol='BTC', network=network).first()
                    #     latest_txs = btc_transaction_history.get_transactions_btc(wallet_address)
                    #
                    # elif wallet_network == 'litecoin':
                    #     print("wallet_network is litecoin")
                    #     network = Network.objects.filter(name='litecoin').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     coin = Coin.objects.filter(symbol='LTC', network=network).first()
                    #     latest_txs = ltc_get_transaction_history.get_transactions_ltc(wallet_address)
                    #
                    # elif wallet_network == 'bch':
                    #     print("wallet_network is bch")
                    #     network = Network.objects.filter(name='bch').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     coin = Coin.objects.filter(symbol='BCH', network=network).first()
                    #     latest_txs = bch_get_transaction_history.get_transactions_bch(wallet_address)
                    #
                    # elif wallet_network == 'doge':
                    #     print("wallet_network is doge")
                    #     network = Network.objects.filter(name='doge').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     coin = Coin.objects.filter(symbol='DOGE', network=network).first()
                    #     latest_txs = doge_get_transaction_history.get_transactions_doge(wallet_address)
                    #
                    # elif wallet_network == 'dash':
                    #     print("wallet_network is dash")
                    #     network = Network.objects.filter(name='dash').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     coin = Coin.objects.filter(symbol='DASH', network=network).first()
                    #     latest_txs = dash_get_transaction_history.get_transactions_dash(wallet_address)

                    if wallet_network == 'cardano':
                        print("wallet_network is cardano")
                        network = Network.objects.filter(name='cardano').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='ADA', network=network).first()
                        latest_txs = cardano_get_transaction_history.get_cardano_history(wallet_address)

                    elif wallet_network == 'xrp':
                        print("wallet_network is xrp")
                        network = Network.objects.filter(name='xrp').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='XRP', network=network).first()
                        latest_txs = xrp_get_transaction_history.get_transactions_xrp(wallet_address)

                    elif wallet_network == 'xlm':
                        print("wallet_network is stellar")
                        network = Network.objects.filter(name='xlm').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='XLM', network=network).first()
                        latest_txs = xlm_get_transaction_history.get_transactions_xlm(wallet_address)

                    elif wallet_network == 'polkadot':
                        print("wallet_network is polkadot")
                        network = Network.objects.filter(name='polkadot').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='DOT', network=network).first()
                        latest_txs = polkadot_get_transaction_history.get_transactions_polkadot(wallet_address)

                    # elif wallet_network == 'dgb':
                    #     print("wallet_network is dgb")
                    #     network = Network.objects.filter(name='dgb').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     coin = Coin.objects.filter(symbol='DGB', network=network).first()
                    #     latest_txs = dgb_get_transaction_history.get_transactions_dgb(wallet_address)
                    #
                    # elif wallet_network == 'zcash':
                    #     print("wallet_network is zcash")
                    #     network = Network.objects.filter(name='zcash').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     coin = Coin.objects.filter(symbol='ZEC', network=network).first()
                    #     latest_txs = zcash_get_transaction_history.get_transactions_zcash(wallet_address)

                    elif wallet_network == 'solana':
                        print("wallet_network is solana")
                        network = Network.objects.filter(name='solana').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='SOL', network=network).first()
                        latest_txs = solana_get_transaction_history.get_transactions_solana(wallet_address)

                    elif wallet_network == 'vechain':
                        print("wallet_network is vechain")
                        network = Network.objects.filter(name='vechain').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='VET', network=network).first()
                        latest_txs = vet_get_transaction_history.get_transactions_vet(wallet_address)

                    elif wallet_network == 'cosmos':
                        print("wallet_network is cosmos")
                        network = Network.objects.filter(name='cosmos').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='ATOM', network=network).first()
                        latest_txs = cosmos_get_transaction_history.get_transactions_cosmos(wallet_address)

                    elif wallet_network == 'theta':
                        print("wallet_network is theta")
                        network = Network.objects.filter(name='theta').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        latest_txs = theta_get_transaction_history.get_transactions_theta(wallet_address)

                    elif wallet_network == 'erc20':
                        print("wallet_network is erc20")
                        network = Network.objects.filter(name='erc20').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        latest_txs = eth_get_transaction_history.get_erc20_history(wallet_address)

                    elif wallet_network == 'trc20':
                        print("wallet network is trc20")
                        network = Network.objects.filter(name='trc20').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        latest_txs = trc20_get_transaction_history.get_trc20_transactions(wallet_address)

                    # elif wallet_network == 'bep20':
                    #     print("wallet_network is bep20")
                    #     network = Network.objects.filter(name='bep20').first()
                    #     wallet = Wallet.objects.filter(address=wallet_address).first()
                    #     latest_txs = bep20_get_transaction_history.get_bep20_history(wallet_address)

                    elif wallet_network == 'bep2':
                        print("wallet_network is bep2")
                        network = Network.objects.filter(name='bep2').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        latest_txs = bep2_get_transaction_history.get_transactions_bep2(wallet_address)

                    elif wallet_network == 'polygon':
                        print("wallet_network is polygon")
                        network = Network.objects.filter(name='polygon').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        latest_txs = polygon_get_transaction_history.get_polygon_history(wallet_address)

                    else:
                        latest_txs = None

                    # Iterate through the transactions and update your database
                    if latest_txs is not None:
                        for tx in latest_txs:
                            print("getting transactions for ", wallet_network)

                            networks_with_coins = (wallet_network == 'erc20' or wallet_network == 'trc20'
                                                   or wallet_network == 'bep2'  # or wallet_network == 'bep20'
                                                   or wallet_network == 'polygon')

                            if networks_with_coins and tx['contract_address'] != '':
                                coin = Coin.objects.filter(contract=tx['contract_address'], network=network).first()
                                if coin is None:
                                    coin = Coin.objects.filter(symbol='no symbol', network=network).first()

                            elif wallet_network == 'erc20' and tx['contract_address'] == '':
                                coin = Coin.objects.filter(symbol='ETH', network=network).first()

                            elif wallet_network == 'trc20' and tx['contract_address'] == '':
                                coin = Coin.objects.filter(symbol='TRX', network=network).first()

                            # elif wallet_network == 'bep20' and tx['contract_address'] == '':
                            #     coin = Coin.objects.filter(symbol='BNB', network=network).first()

                            elif wallet_network == 'bep2' and tx['contract_address'] == '':
                                coin = Coin.objects.filter(symbol='BNB', network=network).first()

                            elif wallet_network == 'polygon' and tx['contract_address'] == '':
                                coin = Coin.objects.filter(symbol='MATIC', network=network).first()

                            elif wallet_network == 'theta' and tx['contract_address'] == 'theta':
                                coin = Coin.objects.filter(symbol='THETA', network=network).first()

                            elif wallet_network == 'theta' and tx['contract_address'] == 'tfuel':
                                coin = Coin.objects.filter(symbol='TFUEL', network=network).first()

                            existing_tx = TransactionHistory.objects.filter(transaction_hash=tx['tx'],
                                                                            transaction_type=tx['type'],
                                                                            amount=tx['amount'], wallet=wallet).first()

                            if not existing_tx:
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
                                pass

                            cache.delete(f'transactions_{wallet_id}')
                    else:
                        print("no transaction received.")

            finally:
                release_lock()


@shared_task(name="update_transactions_bep20")
def update_transactions_bep20():
    with transaction.atomic():
        lock_id = "update_transactions_bep20_lock"
        acquire_lock = lambda: cache.add(lock_id, "true", 60 * 5)
        release_lock = lambda: cache.delete(lock_id)
        if acquire_lock():
            try:
                time_threshold = datetime.now() - timedelta(seconds=60)
                print("updating...")
                # Get all wallets from the database
                wallets = Wallet.objects.all()

                # Loop through each wallet and retrieve the latest transactions
                for wallet in wallets:
                    wallet_id = wallet.id
                    wallet_network = str(wallet.network)
                    wallet_address = str(wallet.address)

                    if wallet_network == 'bep20':
                        print("wallet_network is bep20")
                        network = Network.objects.filter(name='bep20').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        latest_txs = bep20_get_transaction_history.get_bep20_history(wallet_address)

                    else:
                        latest_txs = None

                    # Iterate through the transactions and update your database
                    if latest_txs is not None:
                        for tx in latest_txs:
                            print("getting transactions for ", wallet_network)

                            if wallet_network == 'bep20' and tx['contract_address'] != '':
                                coin = Coin.objects.filter(contract=tx['contract_address'], network=network).first()
                                if coin is None:
                                    coin = Coin.objects.filter(symbol='no symbol', network=network).first()

                            elif wallet_network == 'bep20' and tx['contract_address'] == '':
                                coin = Coin.objects.filter(symbol='BNB', network=network).first()

                            existing_tx = TransactionHistory.objects.filter(transaction_hash=tx['tx'],
                                                                            transaction_type=tx['type'],
                                                                            amount=tx['amount'], wallet=wallet).first()

                            if not existing_tx:
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
                                pass

                            cache.delete(f'transactions_{wallet_id}')
                    else:
                        print("no transaction received.")

            finally:
                release_lock()


@shared_task(name="update_transactions_getblock")
def update_transactions_getblock():
    with transaction.atomic():
        lock_id = "update_transactions_getblock_lock"
        acquire_lock = lambda: cache.add(lock_id, "true", 60 * 5)
        release_lock = lambda: cache.delete(lock_id)
        if acquire_lock():
            try:
                time_threshold = datetime.now() - timedelta(seconds=60)
                print("updating getblock...")
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

                    elif wallet_network == 'doge':
                        print("wallet_network is doge")
                        network = Network.objects.filter(name='doge').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='DOGE', network=network).first()
                        latest_txs = doge_get_transaction_history.get_transactions_doge(wallet_address)

                    elif wallet_network == 'dash':
                        print("wallet_network is dash")
                        network = Network.objects.filter(name='dash').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='DASH', network=network).first()
                        latest_txs = dash_get_transaction_history.get_transactions_dash(wallet_address)

                    elif wallet_network == 'dgb':
                        print("wallet_network is dgb")
                        network = Network.objects.filter(name='dgb').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='DGB', network=network).first()
                        latest_txs = dgb_get_transaction_history.get_transactions_dgb(wallet_address)

                    elif wallet_network == 'zcash':
                        print("wallet_network is zcash")
                        network = Network.objects.filter(name='zcash').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='ZEC', network=network).first()
                        latest_txs = zcash_get_transaction_history.get_transactions_zcash(wallet_address)

                    elif wallet_network == 'harmony':
                        print("wallet_network is harmony")
                        network = Network.objects.filter(name='harmony').first()
                        wallet = Wallet.objects.filter(address=wallet_address).first()
                        coin = Coin.objects.filter(symbol='ONE', network=network).first()
                        latest_txs = harmony_get_transaction_history.get_transactions_harmony(wallet_address)

                    else:
                        latest_txs = None

                    # Iterate through the transactions and update your database
                    if latest_txs is not None:
                        for tx in latest_txs:
                            print("getting transactions for ", wallet_network)
                            existing_tx = TransactionHistory.objects.filter(transaction_hash=tx['tx'],
                                                                            transaction_type=tx['type'],
                                                                            amount=tx['amount'], wallet=wallet).first()

                            if not existing_tx:
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
                                pass

                            cache.delete(f'transactions_{wallet_id}')
                    else:
                        print("no transaction received.")

            finally:
                release_lock()

