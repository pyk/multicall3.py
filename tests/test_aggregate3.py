import pytest
from multicall3 import Multicall3
from web3 import AsyncHTTPProvider
from web3 import AsyncWeb3
from web3 import Web3

from .abi import ERC20_ABI
from .abi import ERC20_BYTES_ABI

w3 = AsyncWeb3(AsyncHTTPProvider("https://ethereum.publicnode.com"))
multicall3 = Multicall3(w3=w3)

USDC = "0xA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48"
MKR = "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2"


@pytest.mark.asyncio
async def test_aggregate3_erc20():
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


@pytest.mark.asyncio
async def test_aggregate3_erc20_bytes():
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(MKR),
        abi=ERC20_BYTES_ABI,
    )

    results = await multicall3.aggregate3(
        contract.functions.name(),
        contract.functions.symbol(),
        contract.functions.decimals(),
    )
    assert (
        results[0]
        == b"Maker\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    assert (
        results[1]
        == b"MKR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    assert results[2] == 18


@pytest.mark.asyncio
async def test_aggregate3_multiple_contracts():
    erc20 = w3.eth.contract(
        address=Web3.to_checksum_address(MKR),
        abi=ERC20_ABI,
    )
    erc20_bytes = w3.eth.contract(
        address=Web3.to_checksum_address(MKR),
        abi=ERC20_BYTES_ABI,
    )

    results = await multicall3.aggregate3(
        erc20.functions.name(),
        erc20_bytes.functions.name(),
        erc20.functions.symbol(),
        erc20_bytes.functions.symbol(),
        erc20_bytes.functions.decimals(),
    )
    assert results[0] is None
    assert (
        results[1]
        == b"Maker\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    assert results[2] is None
    assert (
        results[3]
        == b"MKR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    assert results[4] == 18


@pytest.mark.asyncio
async def test_aggregate3_allow_failure_by_default():
    erc20 = w3.eth.contract(
        address=Web3.to_checksum_address(
            "0x0ba45a8b5d5575935b8158a88c631e9f9c95a2e5"
        ),
        abi=ERC20_ABI,
    )

    results = await multicall3.aggregate3(
        erc20.functions.name(),
        erc20.functions.symbol(),
        erc20.functions.decimals(),
    )
    assert results[0] is None
    assert results[1] is None
    assert results[2] is None
