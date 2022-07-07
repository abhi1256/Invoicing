import json 
from .views import userInvoices
def test_func():
    json_data = open('static/Test.json')   
    Data = json.load(json_data)
    return Data
print(test_func())