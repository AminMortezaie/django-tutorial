from pycardano import Address, PaymentSigningKey, TransactionBuilder, \
    TransactionOutput, BlockFrostChainContext, Network
from blockfrost import ApiUrls
import time

api_key = "previewMT8Y2EIRVvxtKL2Fm14WLue6T6Yo0qSe"
network = Network.TESTNET
context = BlockFrostChainContext(api_key, network, base_url=ApiUrls.preview.value)

# address_from = 'addr_test1vpsyzxs6jej64s4pvhzjt0c4vuze873yx4cwecmjxpdukdsxlf9eg'
# sk_path = 'payment.skey'
# address_to = 'addr_test1vzhplqgqgkds2q6p3ud0ps9gqvas8qnjl7guea0zrj6h6tgtrhl6h'


def submit_transaction(address_from, address_to, amount, signing_key):
    amount = amount * 10**9
    payment_signing_key = PaymentSigningKey.from_json(signing_key)
    tx_builder = TransactionBuilder(context)
    tx_builder.add_input_address(address_from)
    tx_builder.add_output(TransactionOutput.from_primitive([address_to, amount]))
    signed_tx = tx_builder.build_and_sign([payment_signing_key], change_address=Address.from_primitive(address_from))
    context.submit_tx(signed_tx.to_cbor())
    print(context)
    time.sleep(50)
    print(get_transaction_hash(address_from))


def get_transaction_hash(address_from):
    print(context.utxos(str(address_from)))
    transaction_str = str(context.utxos(str(address_from))[0])
    for item in transaction_str.split(":"):
        if "TransactionId(" in item:
            return item.split("(")[1].split('hex=')[1].split('\'')[1]


submit_transaction()