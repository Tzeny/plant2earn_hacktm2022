import pytest
from web3 import Web3 
from ethereum_utils.signature import generate_signature

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545/"))
pk = "872f3dee80ae96e40856c01bdd91cf332e7845aa669e001d335262dd04714a80"

def test_generate_signature():
    signature = generate_signature(w3,pk,"google.com/")
    print(signature)
    assert(signature==(27, 98267571158403538834746466968435380546280106696314277999114650179515406447624, 8920784434310019786291407184895834205834145903176211089264824203047097638167))