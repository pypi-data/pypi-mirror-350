from mongodb_controller import client

DATABASE_NAME_RPA = 'database-rpa'
COLLECTION_NAME_MENU8186 = 'dataset-menu8186'

collection_menu8186 = client[DATABASE_NAME_RPA][COLLECTION_NAME_MENU8186]

def test_menu8186():
    return collection_menu8186.find_one()
