
import pandas as pd
from mongodb_controller import client, COLLECTION_2206, COLLECTION_2205


# 2205: individual portfolio
def create_pipeline_for_latest_date_of_menu2205(fund_code):
    pipeline = [
        {'$match': {'fund_code': fund_code}},
        {'$sort': {'date_ref': -1}},
        {'$project': {'_id': 0, 'date_ref': 1}},
        {'$limit': 1}
    ]
    return pipeline

def get_latest_date_ref_of_menu2205_by_fund_code(fund_code):
    pipeline = create_pipeline_for_latest_date_of_menu2205(fund_code)
    cursor = COLLECTION_2205.aggregate(pipeline)
    return list(cursor)[0]['date_ref']

def create_pipeline_for_menu2205(fund_code, date_ref=None):
    pipeline = [
        {'$match': {'fund_code': fund_code, 'date_ref': date_ref}},
        {'$project': {'_id': 0, 'data': 1}}
    ]
    return pipeline

def fetch_data_menu2205(fund_code, date_ref=None, option_verbose=False):
    date_ref = date_ref if date_ref else get_latest_date_ref_of_menu2205_by_fund_code(fund_code)
    if option_verbose:
        print(f'(fund_code, date_ref): {fund_code, date_ref}')
    pipeline = create_pipeline_for_menu2205(fund_code, date_ref)
    cursor = COLLECTION_2205.aggregate(pipeline)
    return list(cursor)[0]['data']

def fetch_df_menu2205(fund_code, date_ref=None, option_verbose=False):
    data = fetch_data_menu2205(fund_code, date_ref, option_verbose=option_verbose)
    df = pd.DataFrame(data)
    return df


# 2206: total portfolio
def fetch_data_menu2206(fund_code, date_ref=None):
    collection = COLLECTION_2206
    date_ref = date_ref or collection.distinct('일자')[-1]
    pipeline = [
        {'$match': {'일자': date_ref, '펀드코드': fund_code}},
        {'$project': {'_id': 0}}
    ]   
    return list(collection.aggregate(pipeline))

def fetch_df_menu2206(fund_code, date_ref=None):
    data = fetch_data_menu2206(fund_code, date_ref)
    df = pd.DataFrame(data)
    return df

def filter_df_by_valid_assets(df):    
    if df.empty:
        return df
    VALID_ASSETS = ['국내주식', '국내채권', '국내선물', '국내수익증권', '국내수익증권(ETF)', '외화주식', '외화스왑']
    df_filtered = df[df['자산'].isin(VALID_ASSETS)].copy()    
    df_filtered['자산'] = pd.Categorical(df_filtered['자산'], categories=VALID_ASSETS, ordered=True)
    df_sorted = df_filtered.sort_values('자산')
    return df_sorted

COLS_TO_PROJECT = ["자산", "종목", "종목명", "원화 보유정보: 수량", "원화 보유정보: 장부가액", "원화 보유정보: 평가액", "비중: 자산대비", "비중: 시장비중"]
COLS_RENAMED = ["자산", "종목", "종목명", "수량", "장부가", "평가액", "비중", "시장비중"]
MAPPING_COLS = dict(zip(COLS_TO_PROJECT, COLS_RENAMED))

def project_df_by_columns(df, cols=COLS_TO_PROJECT):
    return df[cols]

def rename_df_by_columns(df, cols=COLS_RENAMED):
    return df.rename(columns=MAPPING_COLS)

def run_pipeline_from_raw_to_portfolio(raw):
    df = (
        raw
        .set_index('일자')
        .pipe(filter_df_by_valid_assets)
        .pipe(project_df_by_columns)
        .pipe(rename_df_by_columns)
    )
    return df

def get_df_portfolio(fund_code, date_ref=None):
    raw = fetch_df_menu2206(fund_code, date_ref)
    return run_pipeline_from_raw_to_portfolio(raw)
    