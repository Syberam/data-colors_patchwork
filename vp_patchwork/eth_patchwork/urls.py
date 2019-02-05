from django.urls import path
from .views import EthView, ethTestView

urlpatterns = [
    path('', EthView.as_view() , name='eth'),
    path('nb_blocks/', ethTestView, name='eth_test'),
]