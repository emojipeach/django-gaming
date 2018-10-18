from django import forms
from bets.models import Bet

class BetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bet
        fields = (
        'amount',
        )
