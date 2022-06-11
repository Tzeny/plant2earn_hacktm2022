from ethereum_utils.nft_generator import Generator
import pytest
import json

node_url = "http://127.0.0.1:7545"
private_key = "4e894c66f1ed00237302bada8ba4be2f37c68ba028057e8fcb4c41e7b763ca59"
signer_key = "4e894c66f1ed00237302bada8ba4be2f37c68ba028057e8fcb4c41e7b763ca59" 
contract_address= "0x0238232876955e4CE3EBaFEF5a65299cF194CFb6"
contract_abi = json.loads(open('tests/abi.json').read().replace('\n', ''))

generator = Generator(node_url, private_key, signer_key, contract_address,contract_abi)

def test_generate_nft():
    response = generator.generate_nft("0x510068b3A45905c2B5fac77AA4Ae32444287cB3B","https://google.com")
    print(response)