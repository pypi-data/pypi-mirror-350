from canonical_transformer import get_mapping_of_column_pairs
from fund_insight_engine.fund_data_retriever.menu_data import fetch_menu2210

### IMPORTANT HOTFIX: 8186에는 몇개펀드가 누락됨. 2110으로 대체
### 향후 모든 펀드 기본 정보는 2110을 기준으로 할 예정

def get_mapping_fund_names_mongodb(date_ref=None):
    # date_ref = date_ref or get_latest_date_in_menu8186()
    # cursor = COLLECTION_MENU8186.aggregate(create_pipeline_fund_codes_and_fund_names(date_ref=date_ref))
    # data = list(cursor)
    # mapping_codes_and_names = {datum['펀드코드']: datum['펀드명'] for datum in data}
    mapping_codes_and_names = get_mapping_of_column_pairs(fetch_menu2210(date_ref=date_ref), key_col='펀드코드', value_col='펀드명')
    return mapping_codes_and_names

def get_mapping_fund_inception_dates_mongodb(date_ref=None):
    # date_ref = date_ref or get_latest_date_in_menu8186()
    # cursor = COLLECTION_MENU8186.aggregate(create_pipeline_fund_codes_and_inception_dates(date_ref=date_ref))
    # data = list(cursor)
    # mapping_codes_and_dates = {datum['펀드코드']: datum['설정일'] for datum in data}
    mapping_codes_and_dates = get_mapping_of_column_pairs(fetch_menu2210(date_ref=date_ref), key_col='펀드코드', value_col='설정일')
    return mapping_codes_and_dates
