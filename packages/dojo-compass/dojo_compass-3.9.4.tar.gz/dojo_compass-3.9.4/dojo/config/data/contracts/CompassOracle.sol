// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2;

contract CompassOracle {

    mapping(address => uint256) private assetPrices;
    mapping(address => address) private assetSources;
    address private fallbackOracle;


    function getAssetPrice(address _asset) external view returns (uint256) {
        return assetPrices[_asset];
    }

    function getAssetsPrices(address[] calldata _assets) external view returns(uint256[] memory){
        uint256[] memory prices = new uint256[](_assets.length);
        for (uint256 i = 0; i < _assets.length; i++) {
            prices[i] = assetPrices[_assets[i]];
            // prices[i] = i;
        }
        return prices;
    }
    // Function to set the price of an asset (for testing purposes)
    function setAssetPrice(address _asset, uint256 _price) external {
        assetPrices[_asset] = _price;
    }


    // Function to get the source of a specific asset
    function getSourceOfAsset(address _asset) external view returns (address) {
        return assetSources[_asset];
    }

    // Function to set the source of an asset (for testing purposes)
    function setAssetSource(address _asset, address _source) external {
        assetSources[_asset] = _source;
    }

    function getFallbackOracle() external view returns(address){
        return fallbackOracle;
    }


}