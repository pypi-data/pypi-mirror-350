"""The prediction market representation."""

import datetime

from pydantic import BaseModel

from .outcome_model import OutcomeModel

POLYMARKET_MARKET = "polymarket"
KALSHI_MARKET = "kalshi"
PREDICTIT_MARKET = "predictit"


class PredictionMarketModel(BaseModel):
    """The serialisable prediction market class."""

    question: str
    end_dt: datetime.datetime | None
    outcomes: list[OutcomeModel]
    market: str
