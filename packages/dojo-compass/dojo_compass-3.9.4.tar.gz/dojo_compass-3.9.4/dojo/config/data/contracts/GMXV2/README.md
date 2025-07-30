These contracts are Dojo specific GMX changes required for various functionalities to work, such as keepers.

The general flow is to:
1) modify the existing GMX contract with additions required for dojo to function
2) Compile the contract in `gmx-synthetics` repo
3) copy abis and bytecodes over to dojo
4) replace bytecode of existing contract, such as `OrderHandler` in the GMX environment
5) implement dojo functions to speak to the replaced contracts

In order to find out which libraries are required for compilation, compile bare contract first using:
```
solc contracts/exchange/DojoDepositHandler.sol --base-path . --include-path node_modules/ --include-path node_modules/@openzeppelin/contracts --optimize --bin --abi --storage-layout >> contract.txt
```

`contract.txt` will then have references which libraries are required for contracts/exchange/DojoDepositHandler.sol, for example:

```

// $b63e253a228f0e32f671cc49c7fc32477c$ -> contracts/deposit/DepositStoreUtils.sol:DepositStoreUtils
// $b47f57a87b0fdb80638269130c078613b3$ -> contracts/deposit/DepositUtils.sol:DepositUtils
// $b63e253a228f0e32f671cc49c7fc32477c$ -> contracts/deposit/DepositStoreUtils.sol:DepositStoreUtils
// $b47f57a87b0fdb80638269130c078613b3$ -> contracts/deposit/DepositUtils.sol:DepositUtils
// $a26e5ecaf38b60f56220843100c2d8b777$ -> contracts/deposit/ExecuteDepositUtils.sol:ExecuteDepositUtils
// $b63e253a228f0e32f671cc49c7fc32477c$ -> contracts/deposit/DepositStoreUtils.sol:DepositStoreUtils
// $b63e253a228f0e32f671cc49c7fc32477c$ -> contracts/deposit/DepositStoreUtils.sol:DepositStoreUtils
// $b47f57a87b0fdb80638269130c078613b3$ -> contracts/deposit/DepositUtils.sol:DepositUtils

```

when compiling the deposit handler.

These will then need to be included into compilation of the contract to produce a functional bytecode like:

```
solc contracts/exchange/DojoDepositHandler.sol --libraries "contracts/deposit/DepositStoreUtils.sol:DepositStoreUtils:0x3063A99D2df2A871068D47041eB8d089E5DE1Cdc contracts/deposit/DepositUtils.sol:DepositUtils:0xEb86167C9fEf4534936C523113AB9475a6205559 contracts/deposit/ExecuteDepositUtils.sol:ExecuteDepositUtils:0xbf42A0853266b93A36CF0E367BeAf9a9799d92C6" --base-path . --include-path node_modules/ --include-path node_modules/@openzeppelin/contracts --optimize --bin --abi --storage-layout --output-dir ./tmp/compile_deposit
```