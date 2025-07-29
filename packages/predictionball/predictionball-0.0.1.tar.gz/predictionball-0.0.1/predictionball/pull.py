"""The pull function for fetching the prediction market data."""

from .cluster_model import ClusterModel
from .cluster import cluster
from .kalshi import pull as kalshi_pull
from .polymarket import pull as polymarket_pull
from .predictit import pull as predictit_pull


def pull() -> list[ClusterModel]:
    """Pull the latest economic data."""
    markets = []
    for pull_func in [polymarket_pull, kalshi_pull, predictit_pull]:
        markets.extend(pull_func())
    return cluster(markets)
