// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Coins is ERC20 {
    constructor() ERC20("coins", "MTK") {
        _mint(msg.sender, 2000 * 10 ** decimals());
    }
}