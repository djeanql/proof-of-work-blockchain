from time import time
from hashlib import sha256

from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

class Transaction:
    def __init__(self, pub_key, priv_key, recipient, amount, transaction_type="payment"):
        self.type = transaction_type
        self.sender = pub_key
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time()
        self.signature = None

        self.sign(priv_key)

    @property
    def as_string(self):
        return f"{self.sender}{self.recipient}{self.amount}{self.type}{self.timestamp}"

    @property
    def bytes(self):
        return self.as_string.encode()

    @property
    def txid(self):
        return sha256(self.bytes).hexdigest()

    def sign(self, private_key):
        signing_key = SigningKey(private_key, encoder=HexEncoder)
        self.signature = HexEncoder.encode(signing_key.sign(self.bytes).signature)

    def verify(self):
        signature = HexEncoder.decode(self.signature)
        verify_key = VerifyKey(self.sender, encoder=HexEncoder)

        try:
            verify_key.verify(self.bytes, signature)
        except BadSignatureError:
            return False

        return True
