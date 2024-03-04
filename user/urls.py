from django.urls import path
from .views import *

urlpatterns = [
    path('kayit/', register, name="register"),
    path('cikis/',userLogout, name ="logout"),
    path('profil/<str:slug>', profile, name = "profile"),
    path('yer-isaretleri/', savedTweets, name = "savedTweets"),
    path('duzenle/', change, name = "change"),
    path('back/', back, name = "back")
]
