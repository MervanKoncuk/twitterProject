from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from posts.models import *
from posts.views import userActions
from .forms import *
from django.core.cache import cache
# Create your views here.


def register(request):
  
  
  if request.method == "POST":
    if 'register' in request.POST:
      username = request.POST.get('username')
      name = request.POST.get('name')
      email = request.POST.get('email')
      password1 = request.POST.get('password1')
      password2 = request.POST.get('password2')
      gender = request.POST.get('gender')
      if password1 == password2:
        if User.objects.filter(username = username).exists():
          messages.error(request, 'Bu kullanıcı adı zaten mevcut!')
        elif User.objects.filter(email = email).exists():
          messages.error(request, 'Bu email daha önce kullanılmış!')
        elif len(password1) < 6:
          messages.error(request, 'Şifreniz en az 6 karakter olmalıdır!')
        elif username in password1 or name in password1 or email in password1:
          messages.error(request, 'Şifrenizin ile diğer bilgiler benzer olmamalıdır!')
        elif password1.isnumeric():
          messages.error(request,'Şifreniz sadece sayı içeremez!')
        else:
          user = User.objects.create_user(username = username , email = email, password=password1)
          user.save()
          profile = Profile.objects.create(
            user = user,
            name = name,
          )
          if gender == "female":
            profile.image = "profiles/defImgFemale.png"
          else:
            profile.image = "profiles/defImg.jpg"
          profile.save()
          login(request,user)
          messages.success(request, 'Kaydınız başarıyla oluşturuldu.')
          return redirect('index')
    if 'login' in request.POST:
      username = request.POST.get('username')
      password = request.POST.get('password') 

      user = authenticate(request, username = username, password = password)   

      if user is not None:
        cache_userkey = f"kullanıcı : {username}"
        hata = cache.get(cache_userkey, 0)
        print(hata)
        print(cache_userkey)
        if hata >= 3:
          messages.error(request, 'Hesabınız kilitli olduğu için giriş yapamazsınız')
          return redirect('register')
        login(request, user)
        cache.delete(cache_userkey)
        messages.success(request, 'Giriş Yaptınız.')
        next = request.GET.get('next')
        if next:
          return redirect(next)
        else:
          return redirect('index')
      else:
        cache_userkey = f"kullanıcı : {username}"
        hata = cache.get(cache_userkey, 0)
        hata += 1
        if hata >=3 :
          messages.error(request, 'Üst üste hatalı girdiniz. Hesabınız geçici süreliğine kilitlendi')
          return redirect('register')
        cache.set(cache_userkey, hata, 300)
        messages.error(request, "Kullanıcı adınız veya şifreniz hatalı")
  return render(request, 'user/loginPage.html')

def userLogout(request):
  logout(request)
  messages.success(request, 'Çıkış Yaptınız')
  return redirect('register')


def profile(request, slug):
  meta = request.META.get('HTTP_REFERER') # bir önceki sayfanın linkini çekiyoruz
  cache.set('meta', meta) # meta değişkenini önbelleğe atıyoruz
  profil = Profile.objects.get(slug = slug)
  likes = Post.objects.filter(like__in = [profil]) # postu beğenenler arasında profil olanları filtrele
  retweets = Post.objects.filter(retweet__in = [profil])
  if request.method == 'POST':
    myProfile = request.user.profile
    if 'follow' in request.POST:
      if myProfile in profil.follower.all():
        myProfile.follow.remove(profil)
        profil.follower.remove(myProfile)
      else:
        myProfile.follow.add(profil)
        profil.follower.add(myProfile)  
        yeniBildirim = Notificate(
          receiver = profil,
          sender = myProfile,
          action = 'takip'
        )
        yeniBildirim.message = f"{yeniBildirim.sender.name} kullanıcısı seni takip etmeye başladı"
        yeniBildirim.save()
      profil.save()
      myProfile.save()
      return redirect('profile', slug = profil.slug)
    else:
      userActions(request)
      return redirect('profile', slug = profil.slug)
  context = {
    'profil':profil,
    'likes':likes,
    'retweets':retweets
  }
  return render(request, 'user/profile.html', context)

def savedTweets(request):
  posts = Post.objects.filter(saves__in = [request.user.profile])
  if request.method == 'POST':
    userActions(request)
    return redirect('savedTweets')
  context = {
    'posts':posts
  }
  return render(request, 'explore.html', context)


def change(request):
  profilForm = ProfileForm(instance = request.user.profile)
  username = request.user.username
  email = request.user.email
  if request.method == 'POST':
    if 'update' in request.POST:
      profilForm = ProfileForm(request.POST, request.FILES, instance = request.user.profile)
      newUsername = request.POST.get('username')
      newEmail = request.POST.get('email') # boş olursa none gelir
      if profilForm.is_valid():
        profilForm.save()
        if newUsername and newEmail: # dolu mu 
          if newUsername != username: # yeni girilen kullanıcı adı ile eskisi aynı değilse (yani değiştirildiyse)
            if User.objects.filter(username = newUsername).exists():
              messages.error(request, 'Bu kullanıcı zaten mevcut')
              return redirect('change')
            else:
              request.user.username = newUsername
          if newEmail != email:
            request.user.email = newEmail 
          request.user.save()
          return redirect('profile', slug = request.user.profile.slug)
    if 'change' in request.POST:
      oldPassword = request.POST.get('oldPassword')
      newPassword1 = request.POST.get('newPassword1')
      newPassword2 = request.POST.get('newPassword2')
      
      user = authenticate(request, username = request.user, password = oldPassword)
      
      if user is not None:
        if newPassword1 == newPassword2:
          user.set_password(newPassword1)
          user.save()
          messages.success(request, 'Şifre değiştirildi')
          return redirect('register')
        else:
          messages.error(request, 'Şifreler uyuşmuyor')
      else:
        cache_userkey = f"kullanıcı : {request.user}"
        print(cache_userkey)
        hata = cache.get(cache_userkey, 0)
        hata += 1
        cache.set(cache_userkey, hata, 500)
        if hata == 3:
          logout(request)
          messages.error(request, 'Çok fazla deneme yaptığınız için hesabınız geçici süreliğine kilitlendi')
          return redirect('register')
        
        messages.error(request, 'Mevcut şifrenizi hatalı girdiniz')
      
  context = {
    'profilForm':profilForm,
    'username':username,
    'email':email
  }
  return render(request, 'user/settings.html', context)


def back(request):
  meta = cache.get('meta')
  return redirect(meta)