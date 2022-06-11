from lib2to3.pgen2 import token
from web3 import Web3
from ethereum_utils.signature import generate_signature
from hexbytes import HexBytes

class Generator:
    def __init__(self,node_url, private_key, signer_key, contract_address,contract_abi):
        self.w3 = Web3(Web3.HTTPProvider(node_url))
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
        self.private_key = private_key
        self.signer_key = signer_key

    def generate_transaction(self,user_address,token_uri):
        signature = generate_signature(self.w3,self.signer_key,token_uri)

        address = self.w3.eth.account.privateKeyToAccount(self.private_key).address
        tx_data = {"nonce":self.w3.eth.getTransactionCount(address),"from":address,"gas" : 1300000,"gasPrice": self.w3.toWei("460","gwei")}

        return self.contract.functions["CreateTree"](user=user_address, v=28, r=HexBytes(signature[1]), s=HexBytes(signature[2]), tokenURI=token_uri).buildTransaction(tx_data)

    def sign_transaction(self, transaction):
        return self.w3.eth.account.sign_transaction(transaction, self.private_key)

    def generate_nft(self,user_address,token_uri):
        tx = self.generate_transaction(user_address,token_uri)
        signed_tx = self.sign_transaction(tx)

        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        nft_id = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return nft_id
