from django.urls import path

from . import views

app_name = 'api_viewer'

urlpatterns = [
    # Home page
    path(
        '',
        views.view_event_types,
        name='event_types'
        ),
    # View events
    path(
        'events/<str:event_type_id>/',
        views.view_events,
        name='events'
        ),
    # View events by comp_id
    path(
        'events_competition/<str:comp_id>/',
        views.view_events_competition_id,
        name='events_competition'
        ),
    # View market book
    path(
        'market_book/<str:market_id>/',
        views.view_market_book,
        name='market_book'
        ),
    # View market info
    path(
        'market_info/<str:market_id>/',
        views.view_market_info,
        name='market_info'
        ),
    # View event info
    path(
        'event_info/<str:event_id>/',
        views.view_event_info,
        name='event_info'
        ),
]
