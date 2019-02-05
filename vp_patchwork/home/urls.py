from django.urls import path, include
from .views import Home

urlpatterns = [
    path('', Home, name='home'),
    path('eth/', include('eth_patchwork.urls'), name='eth_patchwork'),
    #path('phone/', include('phone_patchwork.urls'), name='phone_patchwork'),
]