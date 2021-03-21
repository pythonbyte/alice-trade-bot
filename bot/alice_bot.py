"""File that is responsible to handle the operations with the stockbroker API."""
import os
import sys
import requests

from typing import Any, Dict, Optional, Union


class Alice():
    """
    Alice is a bot to send buy and sell signals to a stockbroker platform.

    Using the intercepted data from the quotation client, Alice is used
    to buy/sell the index stocks.
    """

    API_URL = os.environ.get('STOCKBROKER_API_URL', '')
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0'}

    default_payload = {
        'msg[side]': 'SIDE',
        'msg[exchangeordertype]': 'Market',
        'msg[quantity]': '1',
        'msg[symbol]': 'SYMBOL',
        'msg[price]': 0,
        'docket[marketsegment]': 'Futures',
        'token[signature]': os.environ.get('STOCKBROKER_TOKEN'),
        'token[saveforsession]': 'True'
    }

    def __init__(self, paper: str) -> None:
        self.paper = paper
        self._login()

    def _login(self) -> None:
        """Login into the stockbrocker platform."""
        self.session = requests.Session()

        url = os.environ.get('STOCKBROKER_LOGIN_URL', '')
        payload = {
            'ReturnUrl': '',
            'RedirectType': 1,
            'ClientId': os.environ.get('CLIENT_ID', ''),
            'SessionId': os.environ.get('SESSION_ID', ''),
            "Username": os.environ.get('USERNAME', ''),
            "Password": os.environ.get('USER_PASS', ''),
            "DoB": os.environ.get('USER_DOB', ''),
        }
        request = self.session.post(url, data=payload, headers=self.HEADERS)

    def _output_response(self, json_response: dict) -> None:
        """Std out the data from the json response of the API."""
        print(json_response['Timestamp'],
              json_response['Type'],
              json_response['DisplaySide'],
              json_response['DisplayPrice'],
              json_response['Quantity'],
              json_response['DisplaySymbol'])

    def _configure_payload(self, side: str, is_test: bool = False, test_price: int = 0) -> Dict[str, Any]:
        """Setup the proper payload to be sent to the stockbroker API."""
        setup_payload = self.default_payload

        setup_payload['msg[side]'] = side
        setup_payload['msg[symbol]'] = self.paper

        if is_test:
            setup_payload['msg[exchangeordertype]'] = 'Limit'
            setup_payload['msg[price]'] = test_price
        else:
            del setup_payload['msg[price]']

        return setup_payload

    def _send_order(self, setup_payload: dict) -> None:
        """Send the order based on the configured payload."""
        response = self.session.post(self.API_URL, data=setup_payload, headers=self.HEADERS)
        self._output_response(response.json())

    def buy(self) -> None:
        """Send buy signal to the stockbroker API."""
        setup_payload = self._configure_payload('Buy')
        self._send_order(setup_payload)

    def sell(self) -> None:
        """Send sell signal to the stockbroker API."""
        setup_payload = self._configure_payload('Sell')
        self._send_order(setup_payload)

    def reset(self) -> None:
        """Send reset signal to the stockbroker API."""
        setup_payload = self._configure_payload('Reset')
        self._send_order(setup_payload)

    def flip(self) -> None:
        """Send flip signal to the stockbroker API."""
        setup_payload = self._configure_payload('Flip')
        self._send_order(setup_payload)

    def test_buy(self, test_price: int) -> None:
        """Send a test buy signal to the verify stockbroker API return."""
        setup_payload = self._configure_payload('Buy', is_test=True, test_price=test_price)
        self._send_order(setup_payload)


if __name__ == '__main__':
    try:
        stock_paper = sys.argv[1]
        test_price = int(sys.argv[2])
        alice = Alice(stock_paper)
        alice.test_buy(test_price)

    except Exception as exc:
        raise
