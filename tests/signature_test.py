import pytest
from web3 import Web3 
from ethereum_utils.signature import generate_signature

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545/"))
pk = "1950d308895aa7c81523afadacec42743047d78ce27fb0b38cc9c26aae3b3ee2"

def test_generate_signature():
    signature = generate_signature(w3,pk,"google.com/")
    assert(signature==(28, 42968345016949096232418467533464021002017481665278917774776857919597614099140, 14206075651735691821605936562070198693702477194736908795183283155528006488156))