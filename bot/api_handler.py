import base64
import datetime
import json
import traceback

import requests

from balebot.utils.logger import Logger

my_logger = Logger.get_logger()

client_id = 'f741487d-872f-46f8-82ae-b447165d'
client_secret = 'f8e30e8c-cb4c-407e-89cd-fa885a2c9f7c'
redirect_uri = "http://172.31.111.54"

oauth_url = "http://pfm.myoxygen.ir/auth/realms/master/protocol/openid-connect/auth?response_type=code&state=&client_id=f741487d-872f-46f8-82ae-b447165d&client_secret=f8e30e8c-cb4c-407e-89cd-fa885a2c9f7c&scope=&redirect_uri=http://172.31.111.54"


def get_access_token(authorization_code):
    access_token_url = "http://pfm.myoxygen.ir/auth/realms/master/protocol/openid-connect/token"
    authorization = base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')

    headers = {
        'Authorization': "Basic {}".format(authorization),
    }
    body = {
        'grant_type': "authorization_code",
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }
    try:
        response = requests.post(url=access_token_url.format(authorization_code), headers=headers, data=body)
        result = json.loads(response.text)
        print(result)
        # if response.status_code == 200:
        #     if result.get('access_token'):
        #         result = result.get('access_token')
        # else:
        #     result = json.loads('{"error": "not 200"}')
        # else:
        #     result = None
        return result
    except Exception as e:
        traceback.print_exc()
        return json.loads('{"error": "exception"}')


def get_account_information(national_id, access_token):
    url = "http://pfm.myoxygen.ir/api/account/v1/customer/individual/accounts-info"
    headers = {
        'Content-type': 'application/json',
        'Authorization': "Bearer {}".format(access_token),
    }
    body = {
        'nationalIdentifier': national_id
    }
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(body))
        result = json.loads(response.text)
        print(result)
        # if response.status_code == 200:
        #     if result.get('access_token'):
        #         result = result.get('response').get('accounts')
        # else:
        #     result = json.loads('{"error": "not 200"}')
        # else:
        #     result = None
        return result
    except Exception as e:
        traceback.print_exc()
        return json.loads('{"error": "exception"}')


def get_account_transactions(account_number: str, from_datetime, to_datetime, page: int, page_size: int, access_token):
    url = "http://pfm.myoxygen.ir/api/statement/v1/account/transactions"
    headers = {
        'Content-type': 'application/json',
        'Authorization': "Bearer {}".format(access_token),
    }
    body = {
        "accountNumber": account_number,
        "dateRange": {
            "fromDateTime": from_datetime.isoformat()[:-3]+'Z',
            "toDateTime": to_datetime.isoformat()[:-3]+'Z'
        },
        "pageable": {
            "page": page,
            "size": page_size,
        }
    }
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(body))
        result = json.loads(response.text)
        print(result)
        # if response.status_code == 200:
        #     if result.get('access_token'):
        #         result = result.get('response')
        # else:
        #     result = json.loads('{"error": "not 200"}')
        # else:
        #     result = None
        return result
    except Exception as e:
        traceback.print_exc()
        return json.loads('{"error": "exception"}')


def get_account_balance(account_number, access_token):
    url = f"http://pfm.myoxygen.ir/api/sandbox/account/v1/account/balances/{account_number}"
    headers = {
        'Content-type': 'application/json',
        'Authorization': "Bearer {}".format(access_token),
    }
    try:
        response = requests.get(url=url, headers=headers)
        result = json.loads(response.text)
        print(result)
        # if response.status_code == 200:
        #     if result.get('access_token'):
        #         result = result.get('response')
        # else:
        #     result = json.loads('{"error": "not 200"}')
        # else:
        #     result = None
        return result
    except Exception as e:
        traceback.print_exc()
        return json.loads('{"error": "exception"}')


# get_account_balance(account_number="0100001012001",
#                     access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJINGpXcmRDYl9sUHZRbmkwd3ZSOVQ2UkpMNlF2Mmt1V2NSakh4SjFrY2NRIn0.eyJqdGkiOiJlMDU1OTc3NC1mMmE2LTQzZWUtOTA3OC0yZTIzNTg3YTA2YmIiLCJleHAiOjE1NDc3NTU3MjQsIm5iZiI6MCwiaWF0IjoxNTQ3NzIwMDY3LCJpc3MiOiJodHRwOi8vcGZtLm15b3h5Z2VuLmlyL2F1dGgvcmVhbG1zL21hc3RlciIsImF1ZCI6ImY3NDE0ODdkLTg3MmYtNDZmOC04MmFlLWI0NDcxNjVkIiwic3ViIjoiNzhhNmMxMWMtNDg1MC00NjZjLTg0MTYtMzc1NWU4OTJmNjViIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZjc0MTQ4N2QtODcyZi00NmY4LTgyYWUtYjQ0NzE2NWQiLCJhdXRoX3RpbWUiOjE1NDc3MTk3MjQsInNlc3Npb25fc3RhdGUiOiI0Mjc2NmEwYy04Y2EwLTQwMzctYjJlZC05ODIzZTBhMDhmMjIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVzb3VyY2VfYWNjZXNzIjp7IlNCQWNjb3VudFRyYW5zYWN0aW9uIjp7InJvbGVzIjpbInN2Yy1tZ210LWFjY291bnQtdHJ4Il19LCJTQkFjY291bnRCYWxhbmNlIjp7InJvbGVzIjpbInN2Yy1tZ210LWFjY291bnQtYmFsYW5jZSJdfSwiU0JDdXN0b21lckFjY291bnRJbmZvIjp7InJvbGVzIjpbInN2Yy1tZ210LWN1c3RvbWVyLWFjY291bnQiXX19LCJzc24iOiIwNDUwMDkwOTAwIn0.InTrH6gN-P8pnk6HXqZrX7sVSnKv9KXaJPk06NtOuvaKbdL6bjVW-Fxvi8NCXGVtXtNI4xX5OKUwvl1vP_00T31Y1Ldrss5EGfgdRHSBL4ZWEDVPjIO622sw4qMJjJ8-sj8kY_tN_qb50Px-xvYM8GreG-mb17ESVvTy5ll_tLL8aC05JvRi_wbbDPmU3dlbVZE5x_rhY4sqKXp9yr0TeBIEYTw_6g8HMLMu6KJ_GhSnz1yesDzVUPCJTgHv7kfk1z4LFB-pD62cYvvmuK0O94yjGvBr-mZMK7m1x2sAJpYHimD15olNkvTJFDyWi7rRcAwvIjTwEgWQK_B62VkV1w')
# get_account_transactions(account_number="0100001012001",
#                         from_datetime=datetime.datetime.now() - datetime.timedelta(days=365),
#                         to_datetime=datetime.datetime.now(), page=1, page_size=10,
#                         access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJINGpXcmRDYl9sUHZRbmkwd3ZSOVQ2UkpMNlF2Mmt1V2NSakh4SjFrY2NRIn0.eyJqdGkiOiJlMDU1OTc3NC1mMmE2LTQzZWUtOTA3OC0yZTIzNTg3YTA2YmIiLCJleHAiOjE1NDc3NTU3MjQsIm5iZiI6MCwiaWF0IjoxNTQ3NzIwMDY3LCJpc3MiOiJodHRwOi8vcGZtLm15b3h5Z2VuLmlyL2F1dGgvcmVhbG1zL21hc3RlciIsImF1ZCI6ImY3NDE0ODdkLTg3MmYtNDZmOC04MmFlLWI0NDcxNjVkIiwic3ViIjoiNzhhNmMxMWMtNDg1MC00NjZjLTg0MTYtMzc1NWU4OTJmNjViIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZjc0MTQ4N2QtODcyZi00NmY4LTgyYWUtYjQ0NzE2NWQiLCJhdXRoX3RpbWUiOjE1NDc3MTk3MjQsInNlc3Npb25fc3RhdGUiOiI0Mjc2NmEwYy04Y2EwLTQwMzctYjJlZC05ODIzZTBhMDhmMjIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVzb3VyY2VfYWNjZXNzIjp7IlNCQWNjb3VudFRyYW5zYWN0aW9uIjp7InJvbGVzIjpbInN2Yy1tZ210LWFjY291bnQtdHJ4Il19LCJTQkFjY291bnRCYWxhbmNlIjp7InJvbGVzIjpbInN2Yy1tZ210LWFjY291bnQtYmFsYW5jZSJdfSwiU0JDdXN0b21lckFjY291bnRJbmZvIjp7InJvbGVzIjpbInN2Yy1tZ210LWN1c3RvbWVyLWFjY291bnQiXX19LCJzc24iOiIwNDUwMDkwOTAwIn0.InTrH6gN-P8pnk6HXqZrX7sVSnKv9KXaJPk06NtOuvaKbdL6bjVW-Fxvi8NCXGVtXtNI4xX5OKUwvl1vP_00T31Y1Ldrss5EGfgdRHSBL4ZWEDVPjIO622sw4qMJjJ8-sj8kY_tN_qb50Px-xvYM8GreG-mb17ESVvTy5ll_tLL8aC05JvRi_wbbDPmU3dlbVZE5x_rhY4sqKXp9yr0TeBIEYTw_6g8HMLMu6KJ_GhSnz1yesDzVUPCJTgHv7kfk1z4LFB-pD62cYvvmuK0O94yjGvBr-mZMK7m1x2sAJpYHimD15olNkvTJFDyWi7rRcAwvIjTwEgWQK_B62VkV1w')
# get_account_information('0450090900', 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJINGpXcmRDYl9sUHZRbmkwd3ZSOVQ2UkpMNlF2Mmt1V2NSakh4SjFrY2NRIn0.eyJqdGkiOiJlMDU1OTc3NC1mMmE2LTQzZWUtOTA3OC0yZTIzNTg3YTA2YmIiLCJleHAiOjE1NDc3NTU3MjQsIm5iZiI6MCwiaWF0IjoxNTQ3NzIwMDY3LCJpc3MiOiJodHRwOi8vcGZtLm15b3h5Z2VuLmlyL2F1dGgvcmVhbG1zL21hc3RlciIsImF1ZCI6ImY3NDE0ODdkLTg3MmYtNDZmOC04MmFlLWI0NDcxNjVkIiwic3ViIjoiNzhhNmMxMWMtNDg1MC00NjZjLTg0MTYtMzc1NWU4OTJmNjViIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZjc0MTQ4N2QtODcyZi00NmY4LTgyYWUtYjQ0NzE2NWQiLCJhdXRoX3RpbWUiOjE1NDc3MTk3MjQsInNlc3Npb25fc3RhdGUiOiI0Mjc2NmEwYy04Y2EwLTQwMzctYjJlZC05ODIzZTBhMDhmMjIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVzb3VyY2VfYWNjZXNzIjp7IlNCQWNjb3VudFRyYW5zYWN0aW9uIjp7InJvbGVzIjpbInN2Yy1tZ210LWFjY291bnQtdHJ4Il19LCJTQkFjY291bnRCYWxhbmNlIjp7InJvbGVzIjpbInN2Yy1tZ210LWFjY291bnQtYmFsYW5jZSJdfSwiU0JDdXN0b21lckFjY291bnRJbmZvIjp7InJvbGVzIjpbInN2Yy1tZ210LWN1c3RvbWVyLWFjY291bnQiXX19LCJzc24iOiIwNDUwMDkwOTAwIn0.InTrH6gN-P8pnk6HXqZrX7sVSnKv9KXaJPk06NtOuvaKbdL6bjVW-Fxvi8NCXGVtXtNI4xX5OKUwvl1vP_00T31Y1Ldrss5EGfgdRHSBL4ZWEDVPjIO622sw4qMJjJ8-sj8kY_tN_qb50Px-xvYM8GreG-mb17ESVvTy5ll_tLL8aC05JvRi_wbbDPmU3dlbVZE5x_rhY4sqKXp9yr0TeBIEYTw_6g8HMLMu6KJ_GhSnz1yesDzVUPCJTgHv7kfk1z4LFB-pD62cYvvmuK0O94yjGvBr-mZMK7m1x2sAJpYHimD15olNkvTJFDyWi7rRcAwvIjTwEgWQK_B62VkV1w')
# get_access_token(
#     'eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..XVPeT5N4H0PYrqlOzsjBXg.6ob3F4ix3xJrObe3Xpei7UGZI723s1vwj0_c2CXF_UUlM_KSow6gdP3uNgF2WWuCqm2gjBT6z3v5eI9p6QDpNutLcWUd3bugpLYhExzzkf-CT26-byfowGb7YwCmVa_MatfQ-bGYYMMe-UQhZLpwdQztj0oy-12JvjpMfSEZKEU8ivoZ4R7RUM0A6dPTIh1hCmrBhBjckY8vVQJqlCQMwawios4MLEVZ5e2oYb0dukzgYxHu3NzO0KIejfxbw-JB.4jyh8q3vI7wriePDc0xtOg')
