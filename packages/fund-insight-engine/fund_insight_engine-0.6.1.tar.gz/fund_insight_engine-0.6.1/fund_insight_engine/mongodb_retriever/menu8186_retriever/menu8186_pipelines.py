from shining_pebbles import get_yesterday

def create_pipeline_fund_codes_and_fund_names(date_ref=None):
    date_ref = date_ref or get_yesterday()
    return [
        {'$match': {'일자': date_ref}},
        {'$project': {'_id': 0, '펀드코드': 1, '펀드명': 1}}
    ]

def create_pipeline_fund_codes_and_inception_dates(date_ref=None):
    date_ref = date_ref or get_yesterday()
    return [
        {'$match': {'일자': date_ref}},
        {'$project': {'_id': 0, '펀드코드': 1, '설정일': 1}}
    ]

def create_pipeline_of_something(something,date_ref=None):
    date_ref = date_ref or get_yesterday()
    return [
        {'$match': {'일자': date_ref}},
        {'$project': {'_id': 0, '펀드코드': 1, something: 1}}
    ]
