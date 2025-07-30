pragma solidity ^0.8.26;
import "./openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract GenericERC20Token is ERC20 {
    uint8 private _decimals;

    constructor(
        string memory name_,
        string memory symbol_,
        uint8 decimals_
    ) ERC20(name_, symbol_) {
        _decimals = decimals_;
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    function mint(uint256 value) public {
        _update(address(0), msg.sender, value);
    }
}

