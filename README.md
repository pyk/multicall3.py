# multicall3

Python 3 interface for [Multicall3](https://www.multicall3.com/).

## Usage

```python
w3 = AsyncWeb3(AsyncHTTPProvider("https://ethereum.publicnode.com"))

multicall3 = Multicall3(w3=w3)
contract = w3.eth.contract(
    address=Web3.to_checksum_address(USDC),
    abi=ERC20_ABI,
)

results = await multicall3.aggregate3(
    contract.functions.name(),
    contract.functions.symbol(),
    contract.functions.decimals(),
)
assert results[0] == "USD Coin"
assert results[1] == "USDC"
assert results[2] == 6
```

## Contributing

Install `pdm` using [pipx](https://github.com/pypa/pipx):

```shell
pipx install pdm --python $(which python)
```

Install dependencies:

```shell
pdm install
```

Activate the virtualenv:

```shell
$(pdm venv activate)
```

Run the test:

```shell
pytest
```
