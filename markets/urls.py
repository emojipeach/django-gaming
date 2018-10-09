from django.urls import path

from . import views

app_name = 'markets'

urlpatterns = [
    # Add market
    path(
        'add_market/<str:market_id>/',
        views.add_market,
        name='add_market'
        ),
    # View market
    path(
        'view_market/<str:market_id>/',
        views.view_market,
        name='view_market'
        ),
    # Update market
    path(
        'update_market/<str:market_id>/',
        views.update_market,
        name='update_market'
        ),
]
