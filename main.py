from configparser import ConfigParser
import pprint

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators

# Grab configuration values.
config = ConfigParser()
config.read('config/config.ini')

parameters = {}
parameters["api_key"] = config.get('main', 'API_KEY')
parameters["secret_key"] = config.get('main', 'SECRET_KEY')
parameters["base_url"] = config.get('main', 'BASE_URL')
parameters["data_url"] = config.get('main', 'DATA_URL')

# Initalize the robot.
trading_robot = PyRobot("Alpaca", parameters)

# Create a Portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Define mutliple positions to add.
multi_position = [
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'TSLA',
        'purchase_date': '2020-01-31'
    },
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'SQ',
        'purchase_date': '2020-01-31'
    }
]

# Grab the New positions
new_positions = trading_robot.portfolio.add_positions(positions=multi_position)

# Add a single position
trading_robot_portfolio.add_position(
    symbol='MSFT',
    quantity=10,
    purchase_price=10,
    asset_type='equity',
    purchase_date='2020-04-01'
)

# Add another single position
trading_robot_portfolio.add_position(
    symbol='AAPL',
    quantity=10,
    purchase_price=10,
    asset_type='equity',
    purchase_date='2020-04-01'
)

# Print the Positions
pprint.pprint(trading_robot_portfolio.positions)

# Grab the current quotes, for all of our positions.
current_quotes = trading_robot.grab_current_quotes()

# Print the Quotes.
pprint.pprint(current_quotes)