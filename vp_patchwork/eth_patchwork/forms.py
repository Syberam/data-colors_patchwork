from django import forms

class EthForm(forms.Form):
    block_number = forms.CharField()