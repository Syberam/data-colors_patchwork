from django.urls import path
from .views import ethTestView

urlpatterns = [
    path('', ethTestView, name='eth_test'),
]