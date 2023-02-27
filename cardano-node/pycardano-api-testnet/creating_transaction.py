from pycardano import Address, PaymentSigningKey, TransactionBuilder, \
    TransactionOutput, BlockFrostChainContext, Network

from blockfrost import ApiUrls

api_key = "previewsvpVVbnsnUVwPzE9ztGHXtZVKNM1POsJ"
network = Network.TESTNET
context = BlockFrostChainContext(api_key, network, base_url=ApiUrls.preview.value)

address_from = 'addr_test1vpsyzxs6jej64s4pvhzjt0c4vuze873yx4cwecmjxpdukdsxlf9eg'
sk_path = 'payment.skey'
address_to = 'addr_test1vzhplqgqgkds2q6p3ud0ps9gqvas8qnjl7guea0zrj6h6tgtrhl6h'


tx_builder = TransactionBuilder(context)
tx_builder.add_input_address(address_from)
tx_builder.add_output(TransactionOutput.from_primitive([address_to, 1000000000]))
payment_signing_key = PaymentSigningKey.load(sk_path)
signed_tx = tx_builder.build_and_sign([payment_signing_key], change_address=Address.from_primitive(address_from))
print(signed_tx)
context.submit_tx(signed_tx.to_cbor())
print(context)

