from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.http import JsonResponse
from nab_iday.api import NabApi
from nab_iday.models import Place
import json


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
    # Not exactly sure why this is needed in this view but whatevs (breaks
    # if you take it out).
    api = NabApi()
    auth_token = api.login()['tokens'][0]['value']

    return render(request, "transactions.html", {}, context_instance=RequestContext(request))


def transactions_json(request, acc_token):
    api = NabApi()
    auth_token = api.login()['tokens'][0]['value']

    transactions = []
    places = set([])

    for transaction in api.transactions(auth_token, acc_token)['transactionsResponse']['transactions']:
        description = magic_mapper(transaction['description'])
        place, _ = Place.objects.get_or_create(description=description)
        places.add(place)
        transactions.append({
            'date': transaction['date'],
            'description': description,
            'amount': transaction['amount']
        })

    return JsonResponse({
        'transactions': transactions,
        'places': [p.to_json_object() for p in places],
    })


def set_place_state(request):
    json_request = json.loads(request.body.decode('utf-8'))
    place = Place.objects.get(description=json_request['description'])
    place.state = json_request['state']
    place.save()
    return JsonResponse({'status': 'success'})
