"""A puller for polymarket data."""

# pylint: disable=global-statement
import datetime
import logging
import os

from py_clob_client.client import ClobClient  # type: ignore
from py_clob_client.constants import POLYGON  # type: ignore
from py_clob_client.exceptions import PolyApiException  # type: ignore

from .outcome_model import OutcomeModel
from .prediction_market_model import POLYMARKET_MARKET, PredictionMarketModel

_CLOB_CLIENT = None


def _get_clob_client() -> ClobClient:
    global _CLOB_CLIENT
    if _CLOB_CLIENT is None:
        _CLOB_CLIENT = ClobClient(
            "https://clob.polymarket.com", chain_id=POLYGON
        )
    return _CLOB_CLIENT


def pull() -> list[PredictionMarketModel]:
    """Pull the Polymarket prediction market data."""
    logging.info("Pulling Polymarket data")
    client = _get_clob_client()
    cursor = "MA=="
    prediction_markets = []
    try:
        while markets := client.get_markets(next_cursor=cursor):
            if not isinstance(markets, dict):
                raise ValueError("markets is not a dictionary")
            for market in markets["data"]:
                active = market["active"]
                closed = market["closed"]
                end_date = market["end_date_iso"]
                if active and not closed and end_date is not None:
                    prediction_market = PredictionMarketModel(
                        question=market["question"],
                        end_dt=datetime.datetime.fromisoformat(end_date),
                        outcomes=[
                            OutcomeModel(outcome=x["outcome"], price=x["price"])
                            for x in market["tokens"]
                        ],
                        market=POLYMARKET_MARKET,
                    )
                    logging.info(prediction_market)
                    prediction_markets.append(prediction_market)
            cursor = markets["next_cursor"]
            if cursor is None or not cursor:
                break
    except PolyApiException:
        pass
    return prediction_markets
