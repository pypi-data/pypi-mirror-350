"""The outcome representation."""

from pydantic import BaseModel


class OutcomeModel(BaseModel):
    """The serialisable outcome class."""

    outcome: str
    price: float
