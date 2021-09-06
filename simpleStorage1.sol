// SPDX-License-Identifier: MIT
pragma solidity ^0.5.1;

// byzantium

contract SimpleStorage {
    
    mapping (uint256 => uint256) public storageMap;
    
    function setter(uint key, uint value) public {
        storageMap[key] = value;
    }

    function getter(uint key) public view returns (uint) {
        return storageMap[key];
    }
}
