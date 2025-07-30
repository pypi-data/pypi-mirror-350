// SPDX-License-Identifier: BUSL-1.1

pragma solidity ^0.8.0;

import "./DepositHandler.sol";

// This contract needs to be compiled in the same environment as the OrderHandler contract, ie gmx-synthetix repo
// place this file into `contracts/exchange/DojoOrderHandler.sol`
// use:
// solc contracts/exchange/DojoDepositHandler.sol --libraries "contracts/deposit/DepositStoreUtils.sol:DepositStoreUtils:0x3063A99D2df2A871068D47041eB8d089E5DE1Cdc contracts/deposit/DepositUtils.sol:DepositUtils:0xEb86167C9fEf4534936C523113AB9475a6205559 contracts/deposit/ExecuteDepositUtils.sol:ExecuteDepositUtils:0xbf42A0853266b93A36CF0E367BeAf9a9799d92C6" --base-path . --include-path node_modules/ --include-path node_modules/@openzeppelin/contracts --optimize --bin --abi --storage-layout --output-dir ./tmp/compile_deposit

contract DojoDepositHandler is DepositHandler {
    constructor(
        RoleStore _roleStore,
        DataStore _dataStore,
        EventEmitter _eventEmitter,
        Oracle _oracle,
        DepositVault _depositVault
    ) DepositHandler(_roleStore, _dataStore, _eventEmitter, _oracle, _depositVault) {}

    modifier setPricesDojo(
        OracleUtils.SimulatePricesParams memory params
    ) {
        if (params.primaryTokens.length != params.primaryPrices.length) {
            revert Errors.InvalidPrimaryPricesForSimulation(params.primaryTokens.length, params.primaryPrices.length);
        }

        for (uint256 i; i < params.primaryTokens.length; i++) {
            address token = params.primaryTokens[i];
            Price.Props memory price = params.primaryPrices[i];
            oracle.setPrimaryPrice(token, price);
        }

        oracle.setTimestamps(params.minTimestamp, params.maxTimestamp);
        _;
        oracle.clearAllPrices();
    }

    function executeDepositByDojo(
        bytes32 key,
        OracleUtils.SimulatePricesParams memory params
    ) external
        setPricesDojo(params)
    {
        Deposit.Props memory deposit = DepositStoreUtils.get(dataStore, key);
        this._executeDeposit(
            key,
            deposit,
            msg.sender
        );
    }

}