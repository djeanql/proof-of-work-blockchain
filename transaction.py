from time import time
from hashlib import sha256

from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

# TODO: Separate coinbase transaction class

class Transaction:
    def __init__(self, pub_key: str, priv_key: str, recipient: str, amount: float,
        transaction_type: str ="payment"):

        self.type = transaction_type
        self.sender = pub_key
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time()
        self.signature = None

        if priv_key:
            self.sign(priv_key)
    
    def __str__(self):
        return f"{self.sender} ---{self.amount} coins---> {self.recipient}"
    
    @classmethod
    def coinbase(cls, miner_public_key, reward):
        """Returns a coinbase (miner reward) transaction"""
    
        return cls(
            "coinbase",
            None,
            miner_public_key,
            reward,
            transaction_type="coinbase"
        )

    @property
    def as_string(self) -> str:
        return f"{self.sender}{self.recipient}{self.amount}{self.type}{self.timestamp}"

    @property
    def bytes(self) -> bytes:
        return self.as_string.encode()

    @property
    def txid(self) -> str:
        return sha256(self.bytes).hexdigest()

    def sign(self, private_key: str):
        if self.type == "coinbase":
            return

        signing_key = SigningKey(private_key, encoder=HexEncoder)
        self.signature = HexEncoder.encode(signing_key.sign(self.bytes).signature)

    def verify(self) -> bool:
        if self.type == "coinbase":
            return True

        signature = HexEncoder.decode(self.signature)
        verify_key = VerifyKey(self.sender, encoder=HexEncoder)

        try:
            verify_key.verify(self.bytes, signature)
        except BadSignatureError:
            return False

        return True
