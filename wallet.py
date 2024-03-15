from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

import json


class Wallet:
    def __init__(self, file="wallet.json"):
        if not self.load_wallet(file):
            self.create_new_wallet(file)

            print("New wallet.json created.")
        else:
            print("Loaded wallet")

    def load_wallet(self, wallet_file):
        try:
            with open(wallet_file, "r") as f:
                keys = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return False

        self.private_key = keys["private_key"]
        self.public_key = keys["public_key"]

        return True

    def create_new_wallet(self, wallet_file):
        open(wallet_file, "a").close()
        keys = self.generate_keys()
        try:
            with open(wallet_file, "w") as f:
                json.dump(keys, f, indent=4, sort_keys=True)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return False

        self.private_key = keys["private_key"]
        self.public_key = keys["public_key"]

    def generate_keys(self):

        # create public and private RSA keys
        private_key = SigningKey.generate()
        public_key = private_key.verify_key

        keys = {
            "private_key": private_key.encode(encoder=HexEncoder).decode(),
            "public_key": public_key.encode(encoder=HexEncoder).decode(),
        }

        return keys