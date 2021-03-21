"""Initially implementation of Alice using Selenium (deprecated)."""
import os
import sys
import _thread
import datetime
import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class AliceBot:
    """
    Alice bot implementation trough Selenium webdriver.

    The goal is to send buy and sell signals trough the
    Stockbroker webpage.
    """

    def __init__(
            self,
            stock_code: str,
            shares: str,
            username: str,
            password: str,
            dob: str,
            token: str
        ):
        self.stock_code = stock_code
        self.shares = shares
        self.username = username
        self.password = password
        self.dob = dob
        self.token = token

    def _configure_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')

    def _initialize_login(self):
        url = os.environ.get('STOCKBROKER_SELENIUM_URL')

        self.driver.get(url)
        self.driver.find_element_by_xpath("//input[@name='identificationNumber']").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.password)

        date_element = self.driver.find_element_by_id('dob')
        date_element.click()
        date_element.send_keys(self.dob)

        self.driver.find_element_by_xpath('//input[@type="submit"]').click()

    def _configure_stockbroker_page(self):
        selector_url = os.environ.get('STOCKBROKER_SELECTOR_URL')
        day_trade_url = os.environ.get('STOCKBROKER_DAYTRADE_URL')

        self.driver.find_element_by_xpath('//input[@type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.url_to_be(selector_url))

        self.driver.get(day_trade_url)

        # Close popup ads
        close_buttons = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='ipo_close']")))
        self.driver.find_elements_by_class_name

        visible_buttons = [close_button for close_button in close_buttons if close_button.is_displayed()]
        visible_buttons_len = len(visible_buttons)

        for i in range(visible_buttons_len - 1, -1, -1):
            visible_buttons[i].click()

    def _initialize_alice(self):
        self._configure_webdriver()
        self._initialize_login()
        self._configure_stockbroker_page()

        boxes = self.driver.find_elements_by_class_name('box_ativos_01')
        stock_box = [i for i in boxes if self.stock_code in i.text][0]
        stock_box.click()

        shares_input = self.driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[3]/div[1]/div[1]/div[4]/div[6]/div[3]/form/div[1]/div[1]/label/input')
        shares_input.click()
        shares_input.clear()
        shares_input.send_keys(self.shares)

        token_input = self.driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[3]/div[1]/div[1]/div[4]/div[6]/div[3]/form/div[2]/input')
        token_input.click()
        token_input.send_keys(self.token)

    def buy(self):
        """Send buy signal trough the stockbroker webpage."""
        self._initialize_alice()
        buy_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="middle_boleta_fast"]/div[5]/button[1]')))
        buy_btn.click()

    def sell(self):
        """Send sell signal trough the stockbroker webpage."""
        self._initialize_alice()
        sell_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="middle_boleta_fast"]/div[5]/button[2]')))
        sell_btn.click()

    def reset_position(self):
        """Send reset signal trough the stockbroker webpage."""
        self._initialize_alice()
        reset_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="middle_boleta_fast"]/div[5]/button[3]')))
        reset_btn.click()


def alice_send_order(alice: AliceBot, order_type: str):
    """Function to send the order based on the order_type."""
    try:
        if order_type == 'BUY':
            _thread.start_new_thread(alice.buy, ())
        elif order_type == 'SELL':
            _thread.start_new_thread(alice.sell, ())
        elif order_type == 'RESET':
            _thread.start_new_thread(alice.reset_position, ())

    except Exception as e:
        print("Error: unable to start thread")
        logging.error("Exception thread occurred", exc_info=True)


if __name__ == "__main__":
    alice = AliceBot(
        stock_code=sys.argv[1],
        shares=sys.argv[2],
        username=os.environ.get('USERNAME', ''),
        password=os.environ.get('USER_PASS', ''),
        dob=os.environ.get('USER_DOB', ''),
        token=os.environ.get('STOCKBROKER_TOKEN', ''),
    )

    alice_send_order(alice, order_type=sys.argv[3])
