from Crypto.PublicKey import RSA
from Crypto import Random
import transaction
import hashlib


class Transactor:
    """"Implementation of a Block Chain Transactor"""

    def __init__(self, name_in, initial_value_in):
        """Construct a Transactor instance."""
        self.name = name_in

        # Generate Key Pair (Public, Private)
        random_generator = Random.new().read
        self.key = RSA.generate(1024, random_generator)     # Both Public & Private Keys
        self.public_key = self.key.publickey()              # For External Access

        # All Start w/ Empty Local Copy of Blockchain
        self.blockchain = []

        # Unspent Transaction Outputs (UXTO's); Starts w/ Initial Value In
        self.utxo_pool = [transaction.UTXO(None, None, initial_value_in)]

    # Transaction Verification Methods
    def sign_utxo(self, recipient_in, utxo_in):

        # From Satoshi's White Paper:
        # - Each owner transfers the coin to the next by digitally signing
        #   a hash of the previous transaction and the public key of the next owner

        to_sign = hashlib.sha256(str(utxo_in.transaction_hash.hexdigest()).encode('utf-8') + \
                                 str(recipient_in.public_key).encode('utf-8'))

        utxo_in.signature = self.key.sign(str(to_sign.hexdigest()).encode('utf-8'), '')

    def verify_utxo(self, sender_in, utxo_in):

        # From Satoshi's White Paper:
        # - A payee can verify the signatures to verify the chain of ownership.

        to_verify = hashlib.sha256(str(utxo_in.transaction_hash.hexdigest()).encode('utf-8') + \
                                   str(self.public_key).encode('utf-8'))
                                   
        return sender_in.public_key.verify(str(to_verify.hexdigest()), utxo_in.signature)
