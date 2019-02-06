from .forms import EthForm
from django.views.generic.edit import FormView
from django.shortcuts import render
from web3 import Web3, HTTPProvider
from django.http import HttpResponse


def ethTestView(request):
    infura_provider = HTTPProvider('https://ropsten.infura.io')
    web3 = Web3(infura_provider)
    nb_blocks = web3.eth.blockNumber
    context={}
    context['nb_blocks'] = nb_blocks
    blocks =[]
    for i in range(100):
        block = web3.eth.getBlock(nb_blocks)
        nb_blocks = nb_blocks - 1
        blocks.append(block)
    context['blocks'] = blocks
    #context['balance'] = web3.eth.getBalance('0x147facd275fba25635a334b92500a682cef74f33193a67ccf58e77b635aea700')
    context['balance'] = 0
    return (render(request, 'eth_patchwork/ethForm.html', context))