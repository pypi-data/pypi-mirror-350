from .general_pipelines import create_pipeline_for_latest_date
import pandas as pd

def get_latest_date_in_collection(collection, key_for_date):
    cursor = collection.aggregate(create_pipeline_for_latest_date(key_for_date))
    latest_date = list(cursor)[-1][key_for_date]
    return latest_date

def fetch_data_fund_snapshot_by_date(collection, date_ref=None):
    latest_date = get_latest_date_in_collection(collection, 'date_ref')
    date_ref = date_ref if date_ref else latest_date
    pipeline = [
        {'$match': {'date_ref': date_ref}},
        {'$project': {'_id': 0, 'data': 1}}
    ]
    cursor = collection.aggregate(pipeline)
    data = list(cursor)[0]['data']
    return data

def fetch_df_fund_snapshot_by_date(collection, date_ref=None):
    data = fetch_data_fund_snapshot_by_date(collection, date_ref=date_ref)
    df = pd.DataFrame(data)
    return df