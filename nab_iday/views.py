from django.http import HttpResponse

from nab_iday.api import NabApi


def index(request):
    api = NabApi()
    auth_token = api.login()

    html = "<html><body>Hello %s.</body></html>" % auth_token
    return HttpResponse(html)


def accounts(request):
    api = NabApi()
    auth_token = api.login()['tokens'][0]['value']

    html = "<html><body>Accounts:<ul>"
    for account in api.accounts(auth_token)['accountsResponse']:
        html += '<li><a href="/transactions/{0}/">{1}</a> Remaining balance: {2}</li>'.format(
            account['accountToken'], account['accountIdDisplay'], account['currentBalance'])
    html += "</ul></body></html>"

    return HttpResponse(html)


def transactions(request, acc_token):
    api = NabApi()
    auth_token = api.login()['tokens'][0]['value']

    html = "<html><body>Transactions:<ul>"
    for transaction in api.transactions(auth_token, acc_token)['transactionsResponse']['transactions']:
        html += '<li>{0} {1} {2} {3}</li>'.format(
            transaction['date'], transaction['description'], transaction['narrative'], transaction['amount'])
    html += "</ul></body></html>"

    return HttpResponse(html)
