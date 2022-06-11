// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; 

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract Plant2Earn is ERC721URIStorage, Ownable{
  using Counters for Counters.Counter;
  Counters.Counter private _tokenIds;

  address TreeSigner;

  constructor() ERC721("Plant2Earn", "P2E") {
  }


  function setTreeSigner(address signer) public onlyOwner{
    TreeSigner = signer;
  }

  function getTreeSigner() public view returns (address){
    return TreeSigner;
  }

  function CreateTree(address user, uint8 v, bytes32 r, bytes32 s, string memory tokenURI) public returns (uint256){
    //TO DO: Verify the signature

    uint256 newTreeId = _tokenIds.current();
    _mint(user, newTreeId);
    _setTokenURI(newTreeId, tokenURI);

    _tokenIds.increment();
    return newTreeId;
  }
}


