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


def magic_mapper_description(desc):
    return {
        'Mahadev': 'McDonalds',
        'LinkedAccount': 'Pharmacy',
        'Now': 'Bike Shop',
        '$10 6-Jan USav-Ult': 'Coles',
        'Another test': 'Gym',
        'Test': 'Subway',
        '2c now test': 'Other thing 1',
        'Now 1c test': 'Other thing 2',
        '$20 now Usav-Ultra': 'Vegie Shop',
        '$15 now Usav-Ultra': 'Other thing 3',
        '$25 now Usav-Ultra': 'Other thing 4',
        '$.01 Usaver-Ultra': 'Other thing 5',
        '$3 Usaver to Ultra': 'Other thing 6',
        'Test nabdev.com.au': 'Other thing 7',
    }.get(desc, desc)


def magic_mapper_date(transaction, i):
    from datetime import date, timedelta
    return date(2014, 12, 16) + timedelta(days=i)


def transactions(request, acc_token):
    # Not exactly sure why this is needed in this view but whatevs (breaks
    # if you take it out).
    api = NabApi()
    auth_token = api.login()['tokens'][0]['value']

    return render(request, "transactions.html", {}, context_instance=RequestContext(request))


def transactions_json(request, acc_token):
    api = NabApi()
    auth_token = api.login()['tokens'][0]['value']

    ts = api.transactions(auth_token, acc_token)['transactionsResponse']['transactions']

    transactions = []
    places = set([])

    running_total = []
    last_score = 0

    weekly_total = []
    weekly_score = 0
    week_start = None


    date_format_str = "%Y-%m-%dT%H:%M:%SZ"
    def parse_date(date_str):
        from datetime import datetime
        return datetime.strptime(date_str, date_format_str)

    def serialise_date(date):
        return date.strftime(date_format_str)


    for i, transaction in enumerate(sorted(ts, key=lambda t: t['date'])):
        description = magic_mapper_description(transaction['description'])
        current_date = magic_mapper_date(transaction['date'], i)
        place, _ = Place.objects.get_or_create(description=description)
        places.add(place)


        current_score = last_score + place.get_score()
        weekly_score = weekly_score + place.get_score()

        if i < len(ts) - 1:
            next_date = magic_mapper_date(ts[i + 1]['date'], i + 1)
        else:
            next_date = None

        if i == len(ts) - 1 or next_date != current_date:
            running_total.append({
                'date': serialise_date(current_date),
                'score': current_score
            })

        if i == 0:
            week_start = current_date
        elif i == len(ts) - 1 or (next_date - week_start).days > 7:
            weekly_total.append({
                'date': serialise_date(week_start),
                'score': weekly_score
            })
            weekly_score = 0
            week_start = current_date

        last_score = current_score

        transactions.append({
            'date': current_date,
            'description': description,
            'amount': transaction['amount']
        })

    return JsonResponse({
        'transactions': transactions,
        'places': [p.to_json_object() for p in places],
        'runningTotal': running_total,
        'weeklyTotal': weekly_total,
    })


def set_place_state(request):
    json_request = json.loads(request.body.decode('utf-8'))
    place = Place.objects.get(description=json_request['description'])
    place.state = json_request['state']
    place.save()
    return JsonResponse({'status': 'success'})
