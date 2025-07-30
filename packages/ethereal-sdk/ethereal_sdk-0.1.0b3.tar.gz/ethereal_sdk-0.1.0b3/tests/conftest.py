import os
import pytest
from dotenv import load_dotenv
from eth_account import Account
import ethereal

# Force reload of the dotenv file.
# Ensures that env vars in the .env file will overwrite existing values in the environment
load_dotenv(override=True)

# In order for these tests to run the following must be true:
# 1. The .env file must exist in the root directory of the project
# 2. The .env file must contain the following keys:
#    - RPC_URL
#    - PRIVATE_KEY
# 3. The PRIVATE_KEY must have a balance of ETH


@pytest.fixture(scope="session")
def rc():
    """Client for testing."""
    config = {
        "base_url": os.getenv("BASE_URL"),
        "chain_config": {
            "rpc_url": os.getenv("RPC_URL"),
            "private_key": os.getenv("PRIVATE_KEY"),
        },
    }
    rc = ethereal.RESTClient(config)
    assert rc is not None
    assert rc.chain is not None
    return rc


@pytest.fixture(scope="session")
def rc_ro():
    """Read-only client for testing."""
    private_key = os.getenv("PRIVATE_KEY")
    account = Account.from_key(private_key)
    address = account.address

    config = {
        "base_url": os.getenv("BASE_URL"),
        "chain_config": {
            "rpc_url": os.getenv("RPC_URL"),
            "address": address,
        },
    }
    rc = ethereal.RESTClient(config)
    assert rc is not None
    assert rc.chain is not None
    return rc


@pytest.fixture(scope="session")
def ws_base():
    config = {
        "base_url": os.getenv("WS_URL"),
    }
    ws = ethereal.ws.ws_base.WSBase(config)
    ws.open(namespaces=["/", "/v1/stream"])
    assert ws is not None
    return ws


@pytest.fixture(scope="session")
def ws():
    config = {
        "base_url": os.getenv("WS_URL"),
    }
    ws = ethereal.WSClient(config)
    ws.open(namespaces=["/", "/v1/stream"])
    assert ws is not None
    return ws


@pytest.fixture(scope="session")
def sid(rc):
    """Return the subaccount id for the current test."""
    if len(rc.subaccounts) == 0:
        raise ValueError("No subaccounts found for the connected address.")
    return rc.subaccounts[0].id


@pytest.fixture(scope="session")
def sname(rc):
    """Return the subaccount name for the current test."""
    if len(rc.subaccounts) == 0:
        raise ValueError("No subaccounts found for the connected address.")
    return rc.subaccounts[0].name
