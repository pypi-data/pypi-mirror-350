// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.0;

import "./WithdrawalHandler.sol";

// This contract needs to be compiled in the same environment as the WithdrawalHandler contract, ie gmx-synthetics repo
// place this file into `contracts/exchange/DojoWithdrawalHandler.sol`
// use:
// solc contracts/exchange/DojoWithdrawalHandler.sol --libraries "contracts/withdrawal/WithdrawalUtils.sol:WithdrawalUtils:0x8a2e527008b8BEE4B52A7e79140c74fa0f7BE23a contracts/withdrawal/ExecuteWithdrawalUtils.sol:ExecuteWithdrawalUtils:0xdf27d6C139821E2F39ef0E7abF6434df496436B7 contracts/withdrawal/WithdrawalStoreUtils.sol:WithdrawalStoreUtils:0xD521Cb31B14bB9F70D9a59b47D8763336CAD0395 contracts/gas/GasUtils.sol:GasUtils:0x6Bc801bfd1D0B0bd7a17e38c75DdEE92E8FD3130" --base-path . --include-path node_modules/ --include-path node_modules/@openzeppelin/contracts --optimize --bin --abi --storage-layout --output-dir ./tmp/compile

contract DojoWithdrawalHandler is WithdrawalHandler {

    constructor(
        RoleStore _roleStore,
        DataStore _dataStore,
        EventEmitter _eventEmitter,
        Oracle _oracle,
        WithdrawalVault _withdrawalVault
    ) WithdrawalHandler(_roleStore, _dataStore, _eventEmitter, _oracle, _withdrawalVault) 
    {}
    
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

    function executeWithdrawalByDojo(
        bytes32 key,
        OracleUtils.SimulatePricesParams memory params
    ) external 
        setPricesDojo(params)
    {
        uint256 startingGas = gasleft();

        Withdrawal.Props memory withdrawal = WithdrawalStoreUtils.get(dataStore, key);
        uint256 estimatedGasLimit = GasUtils.estimateExecuteWithdrawalGasLimit(dataStore, withdrawal);
        uint256 executionGas = GasUtils.getExecutionGas(dataStore, startingGas);
        GasUtils.validateExecutionGas(dataStore, startingGas, estimatedGasLimit);

        try this._executeWithdrawal{ gas: executionGas }(
            key,
            withdrawal,
            msg.sender,
            ISwapPricingUtils.SwapPricingType.TwoStep
        ) {
        } catch (bytes memory reasonBytes) {
            _handleWithdrawalError(
                key,
                startingGas,
                reasonBytes
            );
        }
    }

} 