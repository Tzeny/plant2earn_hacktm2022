from web3 import Web3 
from eth_account.messages import encode_defunct
from eth_account import Account

def generate_signature(w3,pk,token_uri):
    message = encode_defunct(text=token_uri)
    signed_message =  w3.eth.account.sign_message(message, private_key=pk)
    vrs = (signed_message["v"],signed_message["r"],signed_message["s"])
    return vrs
