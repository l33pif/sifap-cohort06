import pandas as pd
import numpy as np
from datetime import datetime
import dateutil.parser
import requests
import json
import urllib.request

# from pydrive.drive import GoogleDrive 
# from pydrive.auth import GoogleAuth
# import os

# Function to get download url from a endpoint
def get_url(url):
    req_user = requests.get(url)
    d = req_user.json()
    values_view = d.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)
    return first_value

# Function to clean format of datetime
def convert(datetime_string):
    ts = datetime_string.split()
    ts.pop(0)
    for _ in range(5):
      ts.pop(3)
    return ' '.join(ts)

# def drive():
#     headers = {"Authorization": "ya29.a0AfH6SMDxTLXBjDZKAGOyBpNyw21Pz8spR7kqLXw7vrS-vajqryy8YI0Il5tBw6XasQ6_OEp5qvH3LMzxcYU6RAN_LLdaMHPVdP0Oo_-waMoZ2-qw66JTQgHHfT6v2K73Z1m94jqZLmY1d8msue91pntuj0ym90P0-k8"}
#     para = {
#         "name": "##yourfilepath####",
#     }
#     files = {
#         'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
#         'file': open("./sample.png", "rb")
#     }
#     r = requests.post(
#         "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
#         headers=headers,
#         files=files
#     )
#     print(r.text)



def main():
    # Getting the user csv
    endpoint_user = 'https://ancient-fortress-28096.herokuapp.com/api/superAdmin/get-users'
    users_url = get_url(endpoint_user)
    urllib.request.urlretrieve(users_url, 'users.csv')

    # Getting the receipt csv
    endpoint_receipt = 'https://ancient-fortress-28096.herokuapp.com/api/stadistics/getAllTaxReceips'
    receipt_url = get_url(endpoint_receipt)
    urllib.request.urlretrieve(receipt_url, 'receipt.csv')

    # Naming columns of dataframes
    rec_cols = ['taxReceiptId', 'logo', 'createdAt', 'organizationName', 'userFirstName', 'userLastName', 
            'userFiscalId', 'userDigitalSing', 'userPhoneNumber', 'userEmail', 'userAddress', 'contactFisrtName', 
            'contactLastName', 'contactFiscalId', 'contactEmail', 'contactFiscalAct', 'productName', 
            'productDescription', 'productQuantity', 'productPrice', 'taxes', 'currency', 'subtotal', 
            'total', 'methodPayment', 'productId', 'contactId', 'templateId']
    
    users_cols = ['userId', 'email', 'password', 'phoneNumber', 'firstName', 'lastName', 'dateOfBirth', 'city', 
              'state', 'country', 'taxReceiptLimit', 'fiscalId', 'createdAt', 'role', 'fiscalAct', 'createdBy', 
              'active', 'twoFactorActive', 'typeEmail', 'idCountry', 'profile_picture_url']
    
    # Reading csv 
    receipt = pd.read_csv('receipt.csv', names=rec_cols)
    users = pd.read_csv('users.csv', names=users_cols)

    # Transforming dtype - string to datatime
    users['dateOfBirth'] = users['dateOfBirth'].apply(convert)
    users['dateOfBirth'] = pd.to_datetime(users['dateOfBirth'])
    
    # Creating the final dataframe
    final_df = pd.DataFrame(columns=['Age', 'Total', 'MonthOfPurchase', 'Country', 'Product'])

    # Getting the actual date
    now = pd.to_datetime('now')

    # Getting age 
    final_df['Age'] = (now - users['dateOfBirth']).astype('<m8[Y]')

    # Getting total
    final_df['Total'] = receipt['total']

    # Getting moth of purchase
    receipt['createdAt'] = receipt['createdAt'].apply(convert)
    receipt['createdAt'] = pd.to_datetime(receipt['createdAt'])
    final_df['MonthOfPurchase'] = receipt['createdAt'].dt.month

    # Getting country
    final_df['Country'] = users['country']

    # Converting to excel or csv
    #final_df.to_excel('data_sifap.xlsx')
    final_df.to_csv('data_sifap.csv', encoding='utf-8', index=False)

    # drive()

if __name__ == '__main__':
    main()
    

