from pyrobot.broker_base import Broker, Quote, Order

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
        quotes_from_api = self.api.get_latest_quotes(instruments)
        quotes = list()
        for symbol in quotes_from_api:
            quote = quotes_from_api[symbol]
            quotes.append(Quote(symbol, quote.ap, quote._raw["as"], quote.bp, quote.bs))

        return quotes

    def get_orders(self) -> list:
        orders_from_api = self.api.list_orders()
        orders = list()
        for order in orders_from_api:
            orders.append(Order(order.id, order.created_at, order.updated_at, order.submitted_at, order.symbol, order.qty, order.notional, order.side, order.type, order.time_in_force, order.limit_price,
                                order.stop_price, order.trail_price, order.trail_percent, order.status, order.extended_hours))

        return orders

    def get_order(self, order_id) -> Order:
        order_from_api = self.api.get_order(order_id=order_id)
        order = Order(order_id, order_from_api.created_at, order_from_api.updated_at, order_from_api.submitted_at, order_from_api.symbol, order_from_api.notional, order_from_api.side, order_from_api.time_in_force,
                      order_from_api.stop_price, order_from_api.trail_price, order_from_api.trail_percent, order_from_api.status, order_from_api.extended_hours)

        return order

    def place_order(self, order: Order) -> Order:
        order_from_api = self.api.submit_order(order.symbol, order.quantity, order.side, order.type, order.time_in_force, order.limit_price, order.stop_price, order.id, order.extended_hours, trail_price=order.trail_price, trail_percent=order.trail_percent, notional=order.notional)
        newOrder = Order(order_from_api.id, order_from_api.created_at, order_from_api.updated_at, order_from_api.submitted_at, order_from_api.symbol, order_from_api.notional, order_from_api.side, order_from_api.time_in_force,
                      order_from_api.stop_price, order_from_api.trail_price, order_from_api.trail_percent, order_from_api.status, order_from_api.extended_hours)

        return newOrder
