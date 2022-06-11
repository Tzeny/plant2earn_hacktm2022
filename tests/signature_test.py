import pytest
from web3 import Web3 
from ethereum_utils.signature import generate_signature

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545/"))
pk = "4e894c66f1ed00237302bada8ba4be2f37c68ba028057e8fcb4c41e7b763ca59"

def test_generate_signature():
    signature = generate_signature(w3,pk,"google.com/")
    assert(signature==(28, 90019208878562119238971055917327836843685518048119675335661027233205721757796, 7753231571988683913943783939447174464587726347979054353350138222457541075159))