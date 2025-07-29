"""A puller for predictit data."""

# pylint: disable=global-statement,line-too-long
import datetime
import logging

import requests

from .outcome_model import OutcomeModel
from .prediction_market_model import PREDICTIT_MARKET, PredictionMarketModel


def pull() -> list[PredictionMarketModel]:
    """Pull the PredictIt prediction market data."""
    logging.info("Pulling PredictIt data")

    response = requests.get(
        "https://www.predictit.org/api/marketdata/all/", timeout=30.0
    )
    response.raise_for_status()
    data = response.json()
    prediction_markets = []
    for market in data["markets"]:
        end_dt = None
        outcomes = []
        for contract in market["contracts"]:
            if contract["dateEnd"] != "NA":
                end_dt = datetime.datetime.fromisoformat(contract["dateEnd"])
            outcome = OutcomeModel(
                outcome=contract["name"], price=contract["lastTradePrice"]
            )
            outcomes.append(outcome)
        prediction_market = PredictionMarketModel(
            question=market["name"],
            end_dt=end_dt,
            outcomes=outcomes,
            market=PREDICTIT_MARKET,
        )
        prediction_markets.append(prediction_market)
        logging.info(prediction_market)
    return prediction_markets
