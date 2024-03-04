from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from user.models import *
def userActions(request):
  profile = request.user.profile
  postId = request.POST.get('postId')
  tweet = Post.objects.get(id = postId) # tıklanılan posta ulaştık
  yeniBildirim = Notificate(
    receiver = tweet.owner,
    sender = profile,
    post = tweet
  )
  tweet.view.add(profile)
  if 'like' in request.POST:
    if profile in tweet.like.all():
      tweet.like.remove(profile)
    else:
      tweet.like.add(profile)
      yeniBildirim.action = 'begeni'
      yeniBildirim.message = f"{yeniBildirim.sender.name} kullanıcısı {yeniBildirim.post.content} postunuzu beğendi"
      yeniBildirim.save()
    tweet.save()
  if 'retweet' in request.POST:
    if profile in tweet.retweet.all():
      tweet.retweet.remove(profile)
    else:
      tweet.retweet.add(profile)
      yeniBildirim.action = 'retweet'
      yeniBildirim.message = f"{yeniBildirim.sender.name} kullanıcısı {yeniBildirim.post.content} postunuzu retweet etti"
      yeniBildirim.save()
    tweet.save()
  if 'saves' in request.POST:
    if profile in tweet.saves.all():
      tweet.saves.remove(profile)
    else:
      tweet.saves.add(profile)
    tweet.save()

@login_required(login_url = "register")
def index(request): 
  tweets = Post.objects.all()
  
  if request.method == 'POST':
    profile = request.user.profile
    if 'tweetButton' in request.POST:
      post = request.POST.get('post')
      if post == "":
        messages.error(request, "Boş tweet atamazsınız")
        return redirect('index')
      newPost = Post.objects.create(
        owner = profile,
        content = post,
      )
      newPost.save()
      
      messages.success(request, 'Tweetiniz yayınlandı')
      return redirect('index')
    else:
      userActions(request)
      return redirect('index')
  
  context = {
    'tweets':tweets
  }
  return render(request, 'index.html', context)


def comment(request, postSlug):
  post = Post.objects.get(slug = postSlug)
  print(request.path)
  # görüntüleme
  post.view.add(request.user.profile)
  yorumlar = Comment.objects.filter(post = post)
  if request.method == 'POST':
    if request.user.is_authenticated:
      if 'commentButton' in request.POST:
        yorum = request.POST.get('yorumForm')
        
        newComment = Comment.objects.create(
          owner = request.user.profile,
          post = post,
          comment = yorum
        )
        newComment.save()
        yeniBildirim = Notificate(
          receiver = post.owner,
          sender = request.user.profile,
          post = post,
          action = "yorum"
        )
        yeniBildirim.message = f"{post.content} postunuza {yeniBildirim.sender.name} yorum yaptı"
        yeniBildirim.save()
        messages.success(request, 'Yorumunuz yayınlandı')
        return redirect('comment', postSlug = post.slug)
      else:
        userActions(request)
        return redirect('comment', postSlug = post.slug)
    else:
      messages.error(request, 'yorum yapabilmek için giriş yapmalısınız')
  context = {
    'post':post,
    'comments':yorumlar
  }
  return render(request, 'comments.html', context)

def explore(request):
  posts = Post.objects.all().order_by('?')
  if request.method == 'POST':
    userActions(request)
    return redirect('explore')
  context = {
    'posts':posts
  }
  return render(request, 'explore.html', context)


def search(request):
  if request.GET.get('search'):
    search = request.GET.get('search')
    if search[0] == "@":
      search = search[1:] # @ işaretinden sonrasını aldık
      durum = True
      posts = Profile.objects.filter(
        Q(user__username__icontains = search) |
        Q(name__icontains = search)
      ).distinct().order_by('follower')
    else:
      durum = False
      posts = Post.objects.filter(content__icontains = search)
  context = {
    'posts':posts,
    'durum':durum
  }    
  return render(request, 'search.html', context)


def notifications(request):
  bildirimler = Notificate.objects.filter(receiver = request.user.profile).order_by('-created_at')
  if request.method == 'POST':
    for bildirim in bildirimler:
      bildirim.isRead = True
      bildirim.save()
    return redirect('notifications')
  context = {
    'bildirimler':bildirimler
  }
  return render(request, 'notifications.html', context)


def view_404(request, exception):
  return render(request, 'hata.html')

def view_500(request):
  messages.error(request, 'Sayfada bir sorun oluştu. Giriş yapıp tekrar deneyiniz veya bizimle iletişime geçiniz.')
  return redirect("register")