"""A puller for kalshi data."""

# pylint: disable=global-statement,line-too-long
import datetime
import logging
from typing import Any

import requests

from .outcome_model import OutcomeModel
from .prediction_market_model import KALSHI_MARKET, PredictionMarketModel


def _fetch_kalshi_events(cursor: str | None) -> dict[str, Any]:
    url = "https://api.elections.kalshi.com/trade-api/v2/events?limit=200&status=open&with_nested_markets=true"
    if cursor is not None:
        url += f"&cursor={cursor}"
    return requests.get(
        url,
        headers={
            "Accept": "application/json",
        },
        timeout=30.0,
    ).json()


def pull() -> list[PredictionMarketModel]:
    """Pull the Kalshi prediction market data."""
    logging.info("Pulling Kalshi data")

    cursor = None
    prediction_markets = []
    while events := _fetch_kalshi_events(cursor):
        for event in events["events"]:
            end_dt = None
            outcomes = []
            for market in event["markets"]:
                end_dt = datetime.datetime.fromisoformat(market["close_time"])
                outcome = OutcomeModel(
                    outcome=market["yes_sub_title"], price=market["yes_ask"] / 100.0
                )
                outcomes.append(outcome)
            if end_dt is None:
                raise ValueError("end_dt is null")
            prediction_market = PredictionMarketModel(
                question=event["title"],
                end_dt=end_dt,
                outcomes=outcomes,
                market=KALSHI_MARKET,
            )
            prediction_markets.append(prediction_market)
            logging.info(prediction_market)
        cursor = events["cursor"]
        if cursor is None or not cursor:
            break
    return prediction_markets
