import datetime
import json
import urllib.request, urllib.error

from operator import itemgetter

from api_viewer.api_keys import appKey
from api_viewer.api_keys import sessionToken

headers = {
    'X-Application': appKey,
    'X-Authentication': sessionToken,
    'content-type': 'application/json',
    'accept': 'application/json'
    }

api_url = 'https://api.betfair.com/exchange/betting/rest/v1.0/'

def call_api(url, params):
    try:
        req = urllib.request.Request(url, params.encode('utf-8'), headers)
        response = urllib.request.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse

    except urllib.error.URLError:
        print('Oops there is some issue with the request')
    except urllib.error.HTTPError:
        print('Oops there is some issue with the request' + urllib.error.HTTPError.getcode())

def api_operation(operation, params):
    url = api_url + operation
    params_string = json.dumps(params)
    api_response = call_api(url, params_string)
    if api_response is not None:
        api_loads = json.loads(api_response)
    else:
        api_loads = "Empty response"
    return api_loads

def list_event_types():
    operation = 'listEventTypes/'
    params = {
        "filter":{ }
        }
    result = api_operation(operation, params)
    return result

def list_events(eventTypeID):
    operation = 'listEvents/'
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        "filter":{
            "eventTypeIds":[eventTypeID],
            "marketStartTime":{"from": now}
            }}
    api_results = api_operation(operation, params)
    original = []
    for api_result in api_results:
        original.append(api_result['event'])
    result = sorted(original, key=itemgetter('openDate', 'name')) 
    return result

def list_events_competition_id(comp_id):
    operation = 'listEvents/'
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        "filter":{
            "competitionIds":[comp_id],
            "marketStartTime":{"from": now}
            }}
    api_results = api_operation(operation, params)
    original = []
    for api_result in api_results:
        original.append(api_result['event'])
    result = sorted(original, key=itemgetter('openDate')) 
    return result

def list_competitions_text_search(stringy):
    operation = 'listCompetitions/'
    params = {
        "filter":{
            "textQuery": stringy
            }}
    result = api_operation(operation, params)
    return result

def list_competitions(competitionId):
    operation = 'listCompetitions/'
    params = {
        "filter":{
            "competitionIds": [competitionId]
            }}
    result = api_operation(operation, params)
    return result

def list_event_info(event_id):
    operation = 'listMarketCatalogue/'
    params = {
"filter": 
    {"eventIds":[event_id]},
    "maxResults":"200",
    "marketProjection": ["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION","MARKET_START_TIME"]
    }
    
    api_results = api_operation(operation, params)
    result = sorted(api_results, key=itemgetter('totalMatched'), reverse=True) 
    return result

def list_market_info(market_id):
    operation = 'listMarketCatalogue/'
    params = {
"filter": 
    {"marketIds":[market_id]},
    "maxResults":"200","marketProjection": ["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION","MARKET_START_TIME"]
    }
    result = api_operation(operation, params)
    result = result[0]
    return result

def list_market_book(market_id):
    operation = 'listMarketBook/'
    params = {
"marketIds":[market_id],
"priceProjection":{"priceData":["EX_BEST_OFFERS"]
}}
    result = api_operation(operation, params)
    result = result[0]
    return result

def list_full_market_info(market_id):
    market_book = list_market_book(market_id)
    market_info = list_market_info(market_id)
    # Now take latestOdds from market_book and add it to market_info
    for i in range(len(market_info['runners'])):
        if market_info['runners'][i]['selectionId'] == market_book['runners'][i]['selectionId']:
            market_info['runners'][i]['latestOdds'] = market_book['runners'][i]['lastPriceTraded']
    return market_info

# print(list_event_types())

# print(list_events('1'))

# print(list_competitions('10932509'))

# print(list_events_competition_id('10932509'))

# print(list_competitions_text_search('Premier League'))

# print(list_event_info('28906165'))

# print(list_market_info('1.148606880'))

# print(list_market_book('1.148237405'))


