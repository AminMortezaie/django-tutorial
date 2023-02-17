from cosmospy import BIP32DerivationError, seed_to_privkey
from cosmospy import Transaction


base_url = "https://atom.getblock.io/"
api_key = "382d1202-34e8-4b4f-b458-f37df1bff346"


class CosmospyUtilities:
    @staticmethod
    def private_key_from_seed(seed):
        try:
            private_key = seed_to_privkey(seed, path="m/44'/118'/0'/0/0")
            return private_key
        except BIP32DerivationError:
            print("conversion failed.")

    @staticmethod
    def encode_utf8_private_key_for_model(private_key):
        return private_key.decode('latin-1').encode("utf-8")

    @staticmethod
    def private_key_from_seed_for_model(seed):
        private_key = CosmospyUtilities.private_key_from_seed(seed)
        return CosmospyUtilities.encode_utf8_private_key_for_model(private_key)

    @staticmethod
    def decode_private_key_for_request(utf8_private_key):
        return utf8_private_key.decode("utf-8").encode("latin-1")

    class TransactionBuilder:
        def __int__(self, from_address, to_address,  private_key, account_number, sequence, fee, gas, memo, chain_id, sync_mode, amount):
            self.from_address = from_address
            self.to_address = to_address
            self.private_key = private_key
            self.account_number = account_number
            self.sequence = sequence
            self.fee = fee
            self.gas = gas
            self.memo = memo
            self.chain_id = chain_id
            self.sync_mode = sync_mode
            self.amount = amount

        def get_pushable_transaction(self, built_transaction):
            tx = Transaction(
                from_address=built_transaction.from_address,
                privkey=built_transaction.private_key,
                account_num=built_transaction.account_number,
                sequence=built_transaction.sequence,
                fee=built_transaction.fee,
                gas=built_transaction.gas,
                memo=built_transaction.memo,
                chain_id=built_transaction.chain_id,
                sync_mode=built_transaction.sync_mode,
            )
            tx.add_transfer(
                recipient=built_transaction.to_address, amount=built_transaction.amount
            )
            return tx.get_pushable()

    @staticmethod
    def request_transfer_api(from_address, to_address,  private_key, account_number, sequence, fee, gas, memo, chain_id, sync_mode, amount):
        built_transaction = CosmospyUtilities.TransactionBuilder(from_address, to_address,  private_key, account_number, sequence, fee, gas, memo, chain_id, sync_mode, amount)
        CosmospyUtilities.TransactionBuilder.get_pushable_transaction(built_transaction)
