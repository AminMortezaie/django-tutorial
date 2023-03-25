from pycardano import *
from blockfrost import ApiUrls
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BLOCK_FROST_MAINNET_SECOND_API")
network = Network.MAINNET
context = BlockFrostChainContext(api_key, network, base_url="https://cardano-mainnet.blockfrost.io/api")


def submit_transaction(address_from, address_to, amount, signing_key):
    amount = float(amount) * 1000000
    payment_signing_key = PaymentSigningKey.from_json(signing_key)
    tx_builder = TransactionBuilder(context)
    print("tx_builder 1")
    tx_builder.add_input_address(address_from)
    print("tx_builder 2")
    tx_builder.add_output(TransactionOutput.from_primitive([address_to, int(amount)]))
    print("tx_builder 3")
    signed_tx = tx_builder.build_and_sign([payment_signing_key], change_address=Address.from_primitive(address_from))
    context.submit_tx(signed_tx.to_cbor())
    print(context)
    time.sleep(50)
    return get_transaction_hash(address_from)


def get_transaction_hash(address_from):
    print(context.utxos(str(address_from)))
    transaction_str = str(context.utxos(str(address_from))[0])
    for item in transaction_str.split(":"):
        if "TransactionId(" in item:
            return item.split("(")[1].split('hex=')[1].split('\'')[1]


def generate_wallet():
    payment_signing_key = PaymentSigningKey.generate()
    payment_verification_key = PaymentVerificationKey.from_signing_key(payment_signing_key)
    enterprise_address = Address(payment_part=payment_verification_key.hash(),
                                 network=Network.TESTNET)
    return enterprise_address, payment_signing_key
