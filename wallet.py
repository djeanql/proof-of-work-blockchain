from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

import json


class Wallet:
    def __init__(self, file="wallet.json"):
        keys = self.load_wallet(file)
        if not keys:
            keys = self.create_new_wallet(file)

            print("New wallet created.")
        else:
            print("Loaded wallet")

        self.public_key, self.private_key = keys

    @staticmethod
    def load_wallet(wallet_file):
        try:
            with open(wallet_file, "r") as f:
                keys = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return False

        return keys["public_key"], keys["private_key"]

    def create_new_wallet(self, wallet_file):
        open(wallet_file, "a").close()
        keys = self.generate_keys()
        try:
            with open(wallet_file, "w") as f:
                json.dump(keys, f, indent=4, sort_keys=True)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return False

        return keys["public_key"], keys["private_key"]

    @staticmethod
    def generate_keys():
        """create public and private RSA keys"""

        private_key = SigningKey.generate()
        public_key = private_key.verify_key

        keys = {
            "private_key": private_key.encode(encoder=HexEncoder).decode(),
            "public_key": public_key.encode(encoder=HexEncoder).decode(),
        }

        return keys
