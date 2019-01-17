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


# get_access_token(
#     'eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..XVPeT5N4H0PYrqlOzsjBXg.6ob3F4ix3xJrObe3Xpei7UGZI723s1vwj0_c2CXF_UUlM_KSow6gdP3uNgF2WWuCqm2gjBT6z3v5eI9p6QDpNutLcWUd3bugpLYhExzzkf-CT26-byfowGb7YwCmVa_MatfQ-bGYYMMe-UQhZLpwdQztj0oy-12JvjpMfSEZKEU8ivoZ4R7RUM0A6dPTIh1hCmrBhBjckY8vVQJqlCQMwawios4MLEVZ5e2oYb0dukzgYxHu3NzO0KIejfxbw-JB.4jyh8q3vI7wriePDc0xtOg')
