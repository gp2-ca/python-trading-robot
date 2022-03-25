from pyrobot.broker_base import Broker
from td.client import TDClient
from td.utils import TDUtilities

class BrokerTD(Broker):

    def __init__(self, client_id: str, redirect_uri: str, credentials_path: str) -> None:
        super().__init__()

        self.client = TDClient(client_id, redirect_uri, credentials_path)

        # log the client into the new session
        self.client.login()

    def get_quotes(self, instruments: list) -> dict:
        return self.client.get_quotes(instruments)