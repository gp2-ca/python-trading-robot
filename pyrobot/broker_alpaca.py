from pyrobot.broker_base import Broker, Quote

import alpaca_trade_api as tradeapi

class BrokerAlpaca(Broker):

    def __init__(self, api_key: str, secret_key: str, base_url: str, data_url: str) -> None:
        super().__init__()

        self.api = tradeapi.REST(api_key, secret_key, base_url)

    @property
    def regular_market_open(self):
        """Checks if regular market is open.

        Uses the datetime module to create US Regular Market Equity hours in
        UTC time.

        Usage:
        ----
            >>> trading_robot = PyRobot(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            credentials_path=CREDENTIALS_PATH
            )
            >>> market_open_flag = trading_robot.market_open
            >>> market_open_flag
            True

        Returns:
        ----
        bool -- True if market is open, False otherwise.

        """

        clock = self.api.get_clock()

        return clock.is_open

    def get_quotes(self, instruments: list) -> list:
        quotes = self.api.get_latest_quotes(instruments)
        quotes_list = list()
        for symbol in quotes:
            quote = quotes[symbol]
            quotes_list.append(Quote(symbol, quote.ap, quote._raw["as"], quote.bp, quote.bs))

        return quotes_list
