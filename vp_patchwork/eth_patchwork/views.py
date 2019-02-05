from .forms import EthForm
from django.views.generic.edit import FormView
from django.shortcuts import render
from web3 import Web3, HTTPProvider
from django.http import HttpResponse


def ethTestView(request):
    infura_provider = HTTPProvider('https://ropsten.infura.io')
    web3 = Web3(infura_provider)
    nb_blocks = web3.eth.blockNumber
    return (HttpResponse(str(nb_blocks)))


class EthView(FormView):
    template_name = 'ethForm.html'
    form_class = EthForm
    success_url = '/eth'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get(self):
        return (HttpResponse('succeed'))