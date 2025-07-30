from canonical_transformer import get_mapping_of_column_pairs
from fund_insight_engine.fund_data_retriever.menu_data import fetch_menu2210
from fund_insight_engine.fund_data_retriever.fund_codes.classes_consts import (
    VALUES_FOR_CLASS, 
    KEY_FOR_CLASS, 
)
from fund_insight_engine.fund_data_retriever.fund_codes.menu2110_consts import KEY_FOR_FUND_CODE_IN_MENU2110, KEY_FOR_FUND_NAME_IN_MENU2110

def get_dfs_funds_by_class(date_ref=None):
    df = fetch_menu2210(date_ref=date_ref)
    df_code_class = df[[KEY_FOR_FUND_CODE_IN_MENU2110, KEY_FOR_CLASS]]
    dfs = dict(tuple(df_code_class.groupby(KEY_FOR_CLASS)))
    return dfs

def get_df_funds_by_class(key_for_class, date_ref=None):
    dfs = get_dfs_funds_by_class(date_ref=date_ref)
    df = dfs[key_for_class].set_index(KEY_FOR_FUND_CODE_IN_MENU2110)
    return df

def get_df_funds_mothers(date_ref=None):
    return get_df_funds_by_class('운용펀드', date_ref=date_ref)

def get_df_funds_generals(date_ref=None):
    return get_df_funds_by_class('일반', date_ref=date_ref)

def get_df_funds_class(date_ref=None):
    return get_df_funds_by_class('클래스펀드', date_ref=date_ref)

def get_df_funds_nonclassified(date_ref=None):
    return get_df_funds_by_class('-', date_ref=date_ref)

def get_fund_codes_by_class(key_for_class, date_ref=None):
    df = get_df_funds_by_class(key_for_class, date_ref=date_ref)
    return df.index.tolist()

def get_fund_codes_mothers(date_ref=None):
    return get_fund_codes_by_class('운용펀드', date_ref=date_ref)

def get_fund_codes_generals(date_ref=None):
    return get_fund_codes_by_class('일반', date_ref=date_ref)

def get_fund_codes_class(date_ref=None):
    return get_fund_codes_by_class('클래스펀드', date_ref=date_ref)

def get_fund_codes_nonclassified(date_ref=None):
    return get_fund_codes_by_class('-', date_ref=date_ref)
