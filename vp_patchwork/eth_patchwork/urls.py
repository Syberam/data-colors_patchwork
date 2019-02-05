from django.urls import path
from .views import ethTestView

urlpatterns = [
    path('nb_blocks/', ethTestView, name='eth_test'),
]