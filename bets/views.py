import datetime
import pytz

from django.contrib import messages
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from bets.forms import BetForm
from bets.models import Bet
from markets.models import Market
from markets.models import Runner


def place_bet(request, id):
    if request.method != 'POST':
        runner = Runner.objects.get(id=id)
        market = runner.market
        now = datetime.datetime.now(pytz.timezone('UTC'))
        if now > market.start_time:
            raise Http404('Market has started')
        bet = Bet()
        bet.market = market
        bet.runner = runner
        bet.selection_name = runner.selection_name
        bet.odds = runner.latest_odds
        bet.created_at = now
        bet.save()
        form = BetForm(instance=bet)
    else:
        bet = Bet.objects.get(id=id)
        now = datetime.datetime.now(pytz.timezone('UTC'))
        td = now - bet.created_at

        if td.seconds > 120:
            messages.error(request, 'More than 120 seconds have passed, please try again')
            return HttpResponseRedirect(reverse('markets:view_market', args=[bet.market.market_id]))
            
        elif bet.status == 'QUOTE':
            form = BetForm(instance=bet, data=request.POST)
            if form.is_valid():
                confirmed_bet = form.save(commit=False)
                confirmed_bet.status = 'ACTIVE'
                confirmed_bet.save()

        else:
            messages.error(request, 'This bet has already been placed')

        context = {
            'bet': bet,
            }
        return render(request, 'bets/bet_placed.html', context)
    context = {
        'form': form,
        'bet': bet,
    }
    return render(request, 'bets/place_bet.html', context)

def view_bets(request):
    bets = Bet.objects.filter()
    context = {
        'bets': bets,
    }
    return render(request, 'bets/view_bets.html', context)

def view_settled_bets(request):
    bets = Bet.objects.filter(status='WINNER') | Bet.objects.filter(status='LOSER')

    context = {
        'bets': bets,
    }
    return render(request, 'bets/view_bets.html', context)
