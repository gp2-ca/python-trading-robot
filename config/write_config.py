# python 3.x
from configparser import ConfigParser

config = ConfigParser()

config.add_section('main')
config.set('main', 'CLIENT_ID', 'FAKE_CLIENT_ID')
config.set('main', 'REDIRECT_URI', 'FAKE_REDIRECT_URL')
config.set('main', 'JSON_PATH', 'FAKE_PATH')
config.set('main', 'ACCOUNT_NUMBER', 'FAKE_ACCT')
config.set('main', 'API_KEY', 'FAKE_KEY')
config.set('main', 'SECRET_KEY', 'FAKE_SECRET_KEY')
config.set('main', 'BASE_URL', 'FAKE_URL')
config.set('main', 'DATA_URL', 'FAKE_URL')

with open(file='config/config.ini', mode='w') as f:
    config.write(f)