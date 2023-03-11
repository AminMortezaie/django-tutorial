from pycardano import *
from blockfrost import ApiUrls
import time

api_key = "mainnetTnMir0kxWPEcsWRVPOJxiMbiko76u6PU"
network = Network.MAINNET
context = BlockFrostChainContext(api_key, network, base_url=ApiUrls.mainnet.value)


def submit_transaction(address_from, address_to, amount, signing_key):
    amount = float(amount) * 1000000000
    payment_signing_key = PaymentSigningKey.from_json(signing_key)
    if validate_amount(address_from, amount):
        print("balance is sufficient.")
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
    return "Balance is insufficient!"


def get_transaction_hash(address_from):
    print(context.utxos(str(address_from)))
    transaction_str = str(context.utxos(str(address_from))[0])
    for item in transaction_str.split(":"):
        if "TransactionId(" in item:
            return item.split("(")[1].split('hex=')[1].split('\'')[1]


def validate_amount(address_from, amount):
    print("Amount Validation")
    transaction_str = str(context.utxos(str(address_from))[0])
    for item in transaction_str.split(":"):
        if 'multi_asset' in item:
            if int(item.split(",")[0]) > amount:
                return True
            else:
                return False


def generate_wallet():
    payment_signing_key = PaymentSigningKey.generate()
    payment_verification_key = PaymentVerificationKey.from_signing_key(payment_signing_key)
    enterprise_address = Address(payment_part=payment_verification_key.hash(),
                                 network=network)
    return enterprise_address, payment_signing_key




