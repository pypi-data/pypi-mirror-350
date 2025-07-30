#!/bin/bash

rm -rf output/

COMMIT=eb4e8632f781cdc86b4b47c7e80a5066499bd5d8

if [ ! -d openzeppelin-contracts/ ]; then
	git clone git@github.com:OpenZeppelin/openzeppelin-contracts.git
fi

pushd .
cd openzeppelin-contracts
git checkout "$COMMIT"
popd

mkdir output
solc --pretty-json --output-dir output/ --abi --bin --bin-runtime --storage-layout main.sol --evm-version shanghai

find output/ -type f -and -not -name 'GenericERC20Token*' -delete

echo "Please see output in $(pwd)/output"
