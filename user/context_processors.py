from .models import *
import random
from posts.models import *

def get_profiles(request):
    profiles = ""
    
    if request.user.is_authenticated:
        profil = request.user.profile
        my_follow = profil.follow.all() 
        profiles = Profile.objects.filter(follower__in=my_follow).exclude(name=profil.name).distinct()
        profiles_list = list(profiles)
        random.shuffle(profiles_list)
        profiles = profiles_list[:5]
    return {'profiles':profiles}   

def notificate_count(request):
    bildirim_sayi = Notificate.objects.filter(receiver = request.user.profile, isRead = False).count() if request.user.is_authenticated else 0
    return {'bildirim_sayi':bildirim_sayi}