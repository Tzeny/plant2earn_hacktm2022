from ethereum_utils.nft_generator import Generator
import pytest
import json

node_url = "https://ropsten.infura.io/v3/c7d4a7dd4c414d8184e2e7acfe3a9057"
private_key = "872f3dee80ae96e40856c01bdd91cf332e7845aa669e001d335262dd04714a80"
signer_key = "872f3dee80ae96e40856c01bdd91cf332e7845aa669e001d335262dd04714a80" 
contract_address= "0x08AeDa006B3BFAD92AED30f6C79192f9F5D87b4c"
contract_abi = json.loads(open('tests/abi.json').read().replace('\n', ''))

generator = Generator(node_url, private_key, signer_key, contract_address,contract_abi)

def test_generate_nft():
    response = generator.generate_nft("0x09039B0ea5DA24cA9DD9C9ABDeCbbD6ef47C2bBA","https://google.com")
    print(response)