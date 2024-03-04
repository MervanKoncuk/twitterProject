from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('tweet/<str:postSlug>', comment, name = "comment"),
    path('kesfet/', explore, name = "explore"),
    path('search/', search, name = 'search'),
    path('bildirim/', notifications, name = "notifications")
]
