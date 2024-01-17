# multicall3.py

Python 3 interface for [Multicall3](https://www.multicall3.com/).

## Installation

Install via pip:

```shell
pip install multicall3
```

Install via [pdm](https://pdm-project.org/):

```shell
pdm add multicall3
```

## Example

```python
from multicall3 import Multicall3
from web3 import Web3, AsyncWeb3, AsyncHTTPProvider
import asyncio

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

async def main():
  w3 = AsyncWeb3(AsyncHTTPProvider("https://ethereum.publicnode.com"))
  multicall3 = Multicall3(w3=w3)
  usdc_contract = w3.eth.contract(
      address=Web3.to_checksum_address("0xA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48"),
      abi=ERC20_ABI,
  )

  results = await multicall3.aggregate3(
      usdc_contract.functions.name(),
      usdc_contract.functions.symbol(),
      usdc_contract.functions.decimals(),
  )
  assert results[0] == "USD Coin"
  assert results[1] == "USDC"
  assert results[2] == 6

asyncio.run(main())
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
