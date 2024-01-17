import pytest
from multicall3 import Multicall3
from web3 import AsyncHTTPProvider
from web3 import AsyncWeb3
from web3 import Web3

from .abi import ERC20_ABI

w3 = AsyncWeb3(AsyncHTTPProvider("https://ethereum.publicnode.com"))

USDC = "0xA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48"
MKR = "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2"


@pytest.mark.asyncio
async def test_multicall():
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
