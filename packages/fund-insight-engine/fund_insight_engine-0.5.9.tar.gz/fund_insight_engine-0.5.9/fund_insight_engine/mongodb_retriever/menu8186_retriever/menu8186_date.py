from fund_insight_engine.mongodb_retriever.general_utils import get_latest_date_in_collection
from .menu8186_connector import collection_menu8186 as COLLECTION_MENU8186

def get_latest_date_in_menu8186():
    return get_latest_date_in_collection(COLLECTION_MENU8186, '일자')