from fund_insight_engine.fund_data_retriever.timeseries_external.timeseries import Timeseries
from fund_insight_engine.fund_data_retriever.portfolio.portfolio import Portfolio

class Fund:
    def __init__(self, fund_code, start_date=None, end_date=None, date_ref=None):
        self.fund_code = fund_code
        self.start_date = start_date
        self.end_date = end_date
        self.date_ref = self.set_date_ref(date_ref, end_date)
        self._obj_timeseries = None
        self._obj_portfolio = None
        self._load_pipeline()
    
    def set_date_ref(self, date_ref, end_date):
        if date_ref:
            return date_ref
        elif end_date:
            return end_date
    
    def _load_pipeline(self):
        try:
            self._obj_timeseries = Timeseries(fund_code=self.fund_code, start_date=self.start_date, end_date=self.end_date)
            self.timeseries = self._obj_timeseries.get_df()
            self._obj_portfolio = Portfolio(fund_code=self.fund_code, date_ref=self.date_ref)
            self.portfolio = self._obj_portfolio.get_raw_portfolio()
            return True
        except Exception as e:
            print(f'Fund _load_pipeline error: {e}')
            return False
    
    def get_timeseries(self):
        return self.timeseries
    
    def get_portfolio(self):
        return self.portfolio