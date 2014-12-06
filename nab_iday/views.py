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


def magic_mapper(desc):
    return {
        'Mahadev': 'McDonalds',
        'LinkedAccount': 'Pharmacy',
        'Now': 'Bike Shop',
        '$10 6-Jan USav-Ult': 'Coles',
        'Another test': 'Gym',
        'Test': 'Subway',
        '2c now test': '',
        'Now 1c test': '',
        '$20 now Usav-Ultra': 'Vegie Shop',
        '$15 now Usav-Ultra': '',
        '$25 now Usav-Ultra': '',
        '$.01 Usaver-Ultra': '',
        '$3 Usaver to Ultra': '',
        'Test nabdev.com.au': '',
    }.get(desc, desc)

def transactions(request, acc_token):
    api = NabApi()
    auth_token = api.login()['tokens'][0]['value']

    html = "<html><body>Transactions:<ul>"
    for transaction in api.transactions(auth_token, acc_token)['transactionsResponse']['transactions']:
        html += '<li>{0} {1} {2}</li>'.format(
            transaction['date'], magic_mapper(transaction['description']),
            transaction['amount'])
    html += "</ul></body></html>"

    return HttpResponse(html)
