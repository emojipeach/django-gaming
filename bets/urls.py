from django.urls import path

from . import views

app_name = 'bets'

urlpatterns = [
    # Place a bet
    path(
        'place_bet/<str:id>/',
        views.place_bet,
        name='place_bet'
        ),
    # View all bets
    path(
        'view_bets/',
        views.view_bets,
        name='view_bets'
        ),
    # View settled bets
    path(
        'view_settled_bets/',
        views.view_settled_bets,
        name='view_settled_bets'
        ),
]
