import os
import pytest
from dotenv import load_dotenv
from ostium_python_sdk import OstiumSDK
from ostium_python_sdk.config import NetworkConfig


@pytest.fixture(scope="module")
def sdk():
    # Load environment variables
    load_dotenv()

    rpc_url = os.getenv('RPC_URL')
    if not rpc_url:
        raise ValueError("RPC_URL not found in .env file")

    # Initialize SDK with testnet config
    config = NetworkConfig.testnet()
    return OstiumSDK(config)


@pytest.mark.asyncio
async def test_max_leverage_validation_for_btc_usd(sdk):
    max_leverage = await sdk.get_pair_max_leverage(0)
    print(f"max_leverage: {max_leverage}")

    assert max_leverage == pytest.approx(50, abs=1e-5), \
        f"Failed get_pair_max_leverage assertion for BTC/USD"


@pytest.mark.asyncio
async def test_max_leverage_validation_for_eth_usd(sdk):
    max_leverage = await sdk.get_pair_max_leverage(1)
    print(f"max_leverage: {max_leverage}")

    assert max_leverage == pytest.approx(50, abs=1e-5), \
        f"Failed get_pair_max_leverage assertion for BTC/USD"


@pytest.mark.asyncio
async def test_max_leverage_validation_for_ftse_usd(sdk):
    max_leverage = await sdk.get_pair_max_leverage(14)
    print(f"max_leverage: {max_leverage}")

    assert max_leverage == pytest.approx(100, abs=1e-5), \
        f"Failed get_pair_max_leverage assertion for FTSE/USD"


@pytest.mark.asyncio
async def test_max_leverage_validation_for_tsla_usd(sdk):
    max_leverage = await sdk.get_pair_max_leverage(22)
    print(f"max_leverage: {max_leverage}")

    assert max_leverage == pytest.approx(100, abs=1e-5), \
        f"Failed get_pair_max_leverage assertion for TSLA/USD"
