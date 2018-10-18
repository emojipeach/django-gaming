import datetime
import pytz

from django.contrib import messages
from django.shortcuts import render

from api_viewer.utils import list_full_market_info
from bets.models import Bet
from markets.models import Market
from markets.models import Runner

def add_market(request, market_id):
    search = Market.objects.filter(market_id=market_id)
    if not search:
        market_info = list_full_market_info(market_id)
        market = Market()
        market.market_id = market_id
        market.event_id = market_info['event']['id']
        market.country = market_info['event']['countryCode']
        market.sport = market_info['eventType']['name']
        market.competition_name = market_info['competition']['name']
        market.event_name = market_info['event']['name']
        market.market_name = market_info['marketName']
    
        start_time = datetime.datetime.strptime(
        market_info['event']['openDate'],
        "%Y-%m-%dT%H:%M:%S.000Z"
        )
        start_time = pytz.utc.localize(start_time)
        market.start_time = start_time

        market.timezone = market_info['event']['timezone']
        market.number_runners = len(market_info['runners'])
        market.total_matched = 0
        market.last_updated = datetime.datetime.now(pytz.timezone('UTC'))
        market.save()

        for runner in market_info['runners']:
            new_runner = Runner()
            new_runner.market = market
            new_runner.selection_id = runner['selectionId']
            new_runner.selection_name = runner['runnerName']
            new_runner.sort_priority = runner['sortPriority']
            new_runner.latest_odds = runner['latestOdds']
            new_runner.save()

    else:
        messages.error(request, 'Market {0} already added'.format(market_id))
        market = search[0]

    context = {
        'market': market
        }
    return render(request, 'markets/add_market.html', context)


def view_market(request, market_id):
    market = Market.objects.get(market_id=market_id)
    
    runners = Runner.objects.filter(market=market.id).order_by('sort_priority')
    
    context = {
        'market': market,
        'runners':runners,
        }
    return render(request, 'markets/view_market.html', context)

def update_market(request, market_id):
    market = Market.objects.get(market_id=market_id)
    market.update()
    
    runners = Runner.objects.filter(market=market.id).order_by('sort_priority')
    
    context = {
        'market': market,
        'runners':runners,
        }
    return render(request, 'markets/view_market.html', context)


def settle_market(request, market_id):
    market = Market.objects.get(market_id=market_id)
    market.settle()
    if market.settled is True:
        bets = Bet.objects.filter(market=market.id)
        county = 0
        for bet in bets:
            bet.settle()
            county += 1
    
    runners = Runner.objects.filter(market=market.id).order_by('sort_priority')
    
    context = {
        'market': market,
        'runners':runners,
        }
    return render(request, 'markets/view_market.html', context)


def view_markets(request, sport):
    markets = Market.objects.filter(sport__iexact=sport)
    for market in markets:
        market.runners = Runner.objects.filter(market=market.id).order_by('sort_priority')

    context = {
        'markets': markets,
        }
    return render(request, 'markets/view_markets.html', context)
