import requests
import json
import pprint


class ApiError(Exception):
    def __init__(self, response):
        self.response = response


class NabApi(object):
    def __init__(self):
        self.base_url = "https://api.developer.nab.com.au"

    def _make_request(self, path, method, json_body, token=None):
        url = "{}{}".format(self.base_url, path)

        headers = {
            "Content-Type": "application/json",
            "X-Nab-Key": "nab-iday-20141206"
        }
        if token is not None:
            headers["Authorization"] = token

        params = dict(
            url=url,
            method=method,
            headers=headers,
        )

        if json_body is not None:
            params['data'] = json.dumps(json_body)

        r = requests.request(**params)
        if r.status_code != 200:
            raise ApiError(r)
        response_ob = json.loads(r.content.decode("utf-8"))

        pprint.pprint(response_ob)
        print("\n\n\n")
        return response_ob

    def transactions(self, token, account_token):
        return self._make_request(
            path="/banking/ubank/account/{}/transactions/past?v=2".format(account_token),
            method="GET",
            json_body=None,
            token=token
        )

    def accounts(self, token):
        return self._make_request(
            path="/banking/ubank/accounts?v=4",
            method="GET",
            json_body=None,
            token=token
        )

    def login(self):
        return self._make_request(
            path="/init/auth?v=3",
            method="POST",
            json_body={
                "loginRequest": {
                    "lob": "nab",
                    "brand": "nab",
                    "credentials": {
                    "usernamePassword": {
                        "username": "123456789",
                        "password": "123456789"
                    },
                    "apiStructType": "usernamePassword"
                    }
                }
            }
        )
