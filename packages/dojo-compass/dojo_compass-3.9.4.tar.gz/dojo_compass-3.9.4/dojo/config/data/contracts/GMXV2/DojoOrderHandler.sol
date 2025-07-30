// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.0;

import "./OrderHandler.sol";

// This contract needs to be compiled in the same environment as the OrderHandler contract, ie gmx-synthetix repo
// place this file into `contracts/exchange/DojoOrderHandler.sol`
// use:
// solc contracts/exchange/DojoOrderHandler.sol --libraries "contracts/market/MarketStoreUtils.sol:MarketStoreUtils:0xbbf05cF8e1c6548092A6a02c4c5330E76BF0fE2D contracts/order/OrderUtils.sol:OrderUtils:0x989618BE5450B40F7a2675549643E2e2Dab9978A contracts/order/ExecuteOrderUtils.sol:ExecuteOrderUtils:0x0F385cCE0B595394170a7b69E215dBC8dFE04127 contracts/exchange/DojoOrderHandler.sol:OrderStoreUtils:0x67040c411C1b3195361801E9Ad8a91D1Fe9C0BC2 contracts/order/OrderEventUtils.sol:OrderEventUtils:0xB27d78bFAfe4DEbcaD6a3bee7f5B9805Ed178A2B contracts/order/OrderStoreUtils.sol:OrderStoreUtils:0x67040c411C1b3195361801E9Ad8a91D1Fe9C0BC2" --base-path . --include-path node_modules/ --include-path node_modules/@openzeppelin/contracts --optimize --bin --abi --storage-layout --output-dir ./tmp/compile
contract DojoOrderHandler is OrderHandler {

    constructor(
        RoleStore _roleStore,
        DataStore _dataStore,
        EventEmitter _eventEmitter,
        Oracle _oracle,
        OrderVault _orderVault,
        SwapHandler _swapHandler,
        IReferralStorage _referralStorage
    ) OrderHandler(
        _roleStore,
        _dataStore,
        _eventEmitter,
        _oracle,
        _orderVault,
        _swapHandler,
        _referralStorage
    ) {}
    
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

    function executeOrderByDojo(
        bytes32 key,
        OracleUtils.SimulatePricesParams memory params
    ) external 
        setPricesDojo(params)
    {
        Order.Props memory order = OrderStoreUtils.get(dataStore, key);
        this._executeOrder(
            key,
            order,
            msg.sender
        );
    }

} 