from cosmospy import BIP32DerivationError, seed_to_privkey
from cosmospy import Transaction


def private_key_from_seed(seed):
    try:
        private_key = seed_to_privkey(seed, path="m/44'/118'/0'/0/0")
        return private_key
    except BIP32DerivationError:
        print("conversion failed.")


def private_key_from_seed_for_model(seed):
    private_key = private_key_from_seed(seed)
    return encode_utf8_private_key_for_model(private_key)


def encode_utf8_private_key_for_model(private_key):
    return private_key.decode('latin-1').encode("utf-8")


def decode_private_key_for_request(utf8_private_key):
    return utf8_private_key.decode("utf-8").encode("latin-1")

