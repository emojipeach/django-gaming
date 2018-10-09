# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template.defaulttags import register

from api_viewer.utils import list_event_info
from api_viewer.utils import list_event_types
from api_viewer.utils import list_events
from api_viewer.utils import list_events_competition_id
from api_viewer.utils import list_full_market_info
from api_viewer.utils import list_market_book


@register.filter
def get_item(dictionary, key):
    """ This is a custom filter for django templates allowing you to easily get
    a value from a dictionary."""
    return dictionary.get(key)


def view_event_types(request):
    event_types = list_event_types()
    context = {'event_types': event_types}
    return render(request, 'api_viewer/index.html', context)

def view_events_competition_id(request, comp_id):
    events = list_events_competition_id(comp_id)
    context = {'events': events}
    return render(request, 'api_viewer/events.html', context)

def view_events(request, event_type_id):
    events = list_events(event_type_id)
    context = {'events': events}
    return render(request, 'api_viewer/events.html', context)

def view_event_info(request, event_id):
    event_info = list_event_info(event_id)
    context = {'event_info': event_info}
    return render(request, 'api_viewer/event_info.html', context)

def view_market_info(request, market_id):
    market_info = list_full_market_info(market_id)
    context = {
        'market_info': market_info,
        }
    return render(request, 'api_viewer/market_info.html', context)
    
def view_market_book(request, market_id):
    market_book = list_market_book(market_id)
    context = {
        'market_book': market_book,
        }
    return render(request, 'api_viewer/market_book.html', context)

