from .api.heartbeat import heartbeat
from .api.get_post_investment_product_list import get_post_investment_product_list
from .api.get_portfolio_holdings import get_portfolio_holdings
from .api.get_performance_indicators import get_performance_indicators
from .api.get_post_investment_product_net import get_post_investment_product_net
from .api.get_asset_allocation import get_asset_allocation
from .api.private_net import private_net


class Client:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, token='', env='prd'):
        if self._initialized:
            return
        self.token = token
        if env == 'prd':
            self.base_url = "https://gw.datayes.com/aladdin_mof"
        elif env == 'qa':
            self.base_url = "https://gw.datayes-stg.com/mom_aladdin_qa"
        elif env == 'stg':
            self.base_url = "https://gw.datayes-stg.com/mom_aladdin_stg"
        else:
            raise ValueError("error env")
        self._initialized = True
        heartbeat(self)

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }


Client.get_post_investment_product_list = get_post_investment_product_list
Client.get_portfolio_holdings = get_portfolio_holdings
Client.get_performance_indicators = get_performance_indicators
Client.get_post_investment_product_net = get_post_investment_product_net
Client.get_asset_allocation = get_asset_allocation
Client.private_net = private_net
