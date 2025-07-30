from shining_pebbles import get_yesterday
import pandas as pd
from .data_fetcher import DataFetcher


class Portfolio:
    def __init__(self, fund_code, date_ref=None, option_verbose=False):
        self.fund_code = fund_code
        self.date_ref = date_ref
        self.option_verbose = option_verbose
        self.data_fetcher = None
        self.raw = None
        self.df = None
        self._load_pipeline()
    
    def load_fetcher(self):
        if self.data_fetcher is None:
            data_fetcher = DataFetcher(fund_code=self.fund_code, date_ref=self.date_ref, option_verbose=self.option_verbose)
            self.date_ref = data_fetcher.date_ref
            self.data_fetcher = data_fetcher
        return self.data_fetcher

    def get_raw_portfolio(self):
        if self.raw is None:
            data_fetcher = self.load_fetcher()
            df = data_fetcher.df.set_index('일자')
            dfs = dict(tuple(df.groupby('자산')))
            self.raws = dfs
            valid_assets = ['국내주식', '국내채권', '국내선물', '국내수익증권', '국내수익증권(ETF)', '외화주식', '외화스왑']
            valid_raws = []
            for asset in valid_assets:
                if asset in dfs.keys():
                    valid_raws.append(dfs[asset])
            if len(valid_raws) == 0:
                raw = pd.DataFrame()
            else:
                raw = pd.concat(valid_raws, axis=0)
                raw = raw[raw['종목명']!='소계']
            self.raw = raw
        return self.raw
    
    def get_df(self):
        if self.df is None:
            COLS_FOR_COMPARISON = ['종목명', '종목', '비중: 자산대비']
            self.df = self.get_raw_portfolio()[COLS_FOR_COMPARISON].set_index('종목')
        return self.df

    def _load_pipeline(self):
        try:
            self.get_raw_portfolio()
            self.get_df()
            return True
        except Exception as e:
            print(f'Portfolio _load_pipeline error: {e}')
            return False
    