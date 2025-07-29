"""The cluster representation."""

from pydantic import BaseModel

from .prediction_market_model import PredictionMarketModel


class ClusterModel(BaseModel):
    """The serialisable cluster class."""

    markets: list[PredictionMarketModel]
