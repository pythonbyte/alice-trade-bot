"""File responsible for having the logic for retrieving the stock quotation values."""
import datetime
import json
import requests
import os
import sys

from typing import Optional, Tuple


HEADERS = {'Content-Type': 'application/json',
           'User-Agent': 'Mozilla/5.0'}


def login() -> requests.Session:
    """Function responsible to login and create session for get quotation api."""
    url = os.environ.get('QUOTATION_LOGIN_URL', '')
    payload =  json.dumps({
        'username': os.environ.get('QUOTATION_USERNAME'),
        'password': os.environ.get('QUOTATION_PASSWORD'),
        'id_contract': 2020,
        'channel': '13',
        'info': {
            'os_version': '',
            'version': '',
            'os_name': '',
        }
    })
    session = requests.Session()
    response = session.post(url, data=payload, headers=HEADERS)
    return session


def get_quotation(
        paper: str,
        size: int = 10,
        session: Optional[requests.Session] = None
    ) -> Tuple[requests.Response, requests.Session]:
    """
    Function responsible for getting the stock quotation.

    It will send the payload with the stock paper and return a response
    and a session for future use.
    """
    url = os.environ.get('QUOTATION_URL', '')
    payload = json.dumps({
        'annotations': False,
        'count': size,
        'cd_stock': paper,
        'currency': 'REAL',
        'documents': False,
        'events': False,
        'id_exchange': 1,
        'id_template': 154299,
        'since': 999_999_999_999,
        'tbbar': 'oneminute'
    })
    if not session:
        session = login()

    response = session.post(url, data=payload, headers=HEADERS)
    return response, session


def test_client(stock_paper: str = '') -> None:
    """A simple test function to pull the data from the API."""
    while datetime.datetime.now().second != 2:
        response, session = get_quotation(stock_paper)
        print(response.json()['result']['candles'][0]['vl_close'])
        break


if __name__ == '__main__':
    test_client(stock_paper=sys.argv[1])
