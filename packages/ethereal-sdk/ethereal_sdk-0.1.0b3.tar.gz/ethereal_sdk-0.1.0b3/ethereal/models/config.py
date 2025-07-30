from typing import Optional
from pydantic import BaseModel, Field, AnyHttpUrl, AnyWebsocketUrl


class BaseConfig(BaseModel):
    """Base client configuration model."""

    verbose: bool = False


class HTTPConfig(BaseConfig):
    """HTTP client configuration model."""

    base_url: AnyHttpUrl = Field(
        default=AnyHttpUrl("https://api.etherealtest.net"), description="Base API URL"
    )
    timeout: int = Field(default=30, gt=0, description="Request timeout in seconds")
    rate_limit_headers: bool = Field(
        default=False, description="Include rate limit headers in responses"
    )


class WSBaseConfig(BaseConfig):
    """Base Websocket client configuration model."""

    base_url: AnyWebsocketUrl = Field(
        default=AnyWebsocketUrl("wss://ws.etherealtest.net/"), description="Base WS URL"
    )


class ChainConfig(BaseConfig):
    """Blockchain configuration model."""

    rpc_url: AnyHttpUrl = Field(default=..., description="RPC endpoint URL")
    address: Optional[str] = Field(
        default=None, description="Blockchain address for transactions"
    )
    private_key: Optional[str] = Field(
        default=None, description="Private key for blockchain transactions"
    )


class RESTConfig(HTTPConfig):
    """REST client configuration model."""

    chain_config: Optional[ChainConfig] = Field(
        default=None, description="Blockchain client configuration"
    )
    default_time_in_force: str = Field(
        default="GTD", description="Default time in force for orders"
    )
    default_post_only: bool = Field(
        default=False, description="Default post-only flag for orders"
    )


class WSConfig(WSBaseConfig):
    """Websocket client configuration model."""

    pass
