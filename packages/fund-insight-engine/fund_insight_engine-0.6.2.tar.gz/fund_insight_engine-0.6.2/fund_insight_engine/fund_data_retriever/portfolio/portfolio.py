from shining_pebbles import get_yesterday
import pandas as pd
from .portfolio_fetcher import (
    fetch_df_menu2206,
    run_pipeline_from_raw_to_portfolio,
)
from .portfolio_customizer import customize_df_portfolio

class Portfolio:
    def __init__(self, fund_code, date_ref=None, option_verbose=False):
        self.fund_code = fund_code
        self.date_ref = date_ref
        self.option_verbose = option_verbose
        self.raw = None
        self.df = None
        self.port = None
        self._load_pipeline()

    def get_raw(self):
        if self.raw is None:
            self.raw = fetch_df_menu2206(self.fund_code, self.date_ref)
        return self.raw

    def get_df(self):
        if self.df is None:
            self.df = run_pipeline_from_raw_to_portfolio(self.get_raw())
        return self.df

    def get_customized_port(self):
        if self.port is None:
            self.port = customize_df_portfolio(self.get_df())
        return self.port

    def _load_pipeline(self):
        try:
            self.get_raw()
            self.get_df()
            self.get_customized_port()
            return True
        except Exception as e:
            print(f'Portfolio _load_pipeline error: {e}')
            return False
    