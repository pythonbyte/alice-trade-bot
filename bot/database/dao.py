"""File to abstract the connection with db and models."""
from sqlalchemy import desc
from typing import Dict, Any

from db import Stock, Token, Session

session = Session()


def insert_stock_values(values: Dict[str, Any]) -> None:
    """Function to save on database the stock values."""
    stock = Stock(**values)
    session.add(stock)
    session.commit()


def insert_token(values: Dict[str, Any]) -> None:
    """Function to save on database the tocken values."""
    token = Token(**values)
    session.add(token)
    session.commit()


def get_last_token(platform: str) -> Token:
    """Function to retrieve the last token saved."""
    token = (session.query(Token)
             .filter(Token.platform == platform)
             .order_by(desc(Token.date))
             .first())
    return token
