from django.urls import path
from .views import MyView, Test2015View, viewInitDb, viewFeedDb, SearchView

urlpatterns = [
    path('', SearchView.as_view(), name='search_home'),
    path('auth/', MyView.as_view(), name='home'),
    path('test/', Test2015View.as_view(), name='test'),
    path('init_db/', viewInitDb, name='init_db'),
    path('feed_db/', viewFeedDb, name='feed_db'),
]
