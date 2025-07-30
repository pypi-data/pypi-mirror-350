from mongodb_controller.mongodb_collections import COLLECTION_RPA
from fund_insight_engine.mongodb_retriever.general_utils import fetch_df_fund_snapshot_by_date

def fetch_menu2210(date_ref=None):
    collection = COLLECTION_RPA['2110']
    return fetch_df_fund_snapshot_by_date(collection, date_ref=date_ref)
