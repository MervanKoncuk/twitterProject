from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
# paste this at the start of code

# Create your models here.
class Post(models.Model):
  id = models.UUIDField(primary_key = True, unique = True, db_index = True, default = uuid.uuid4, editable= False)
  owner = models.ForeignKey('user.Profile', on_delete = models.CASCADE, verbose_name ="Yazar")
  content = models.TextField(verbose_name = "Tweet")
  image = models.ImageField(upload_to='posts/', verbose_name="Resim", blank=True, null = True)
  like = models.ManyToManyField('user.Profile',related_name="likes", verbose_name="Beğenenler", blank=True, symmetrical= False)
  saves = models.ManyToManyField('user.Profile',related_name="saves", verbose_name="Kaydedenler", blank=True)
  retweet = models.ManyToManyField('user.Profile',related_name="retweet", verbose_name="Retweet", blank=True)
  view = models.ManyToManyField('user.Profile', related_name="views", verbose_name="Görüntüleyenler", blank=True)
  created_at = models.DateTimeField(auto_now_add = True, verbose_name = "Oluşturulma Tarihi")
  slug = models.SlugField(blank= True, null= True)

  def __str__(self):
      return self.owner.name

  def save(self, *args, **kwargs):
    self.slug = slugify(self.content.replace('ı', 'i'))
    super().save(*args, **kwargs)
  
  class Meta:
     verbose_name_plural = "Tweetler"
     verbose_name = "Tweet"
     ordering = ["-created_at"]  
     
# Yorum yapan
# yorum yapılan post
# yorum yaptığı tarih
# yorum    
class Comment(models.Model):
  id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
  owner = models.ForeignKey('user.Profile', on_delete = models.CASCADE, verbose_name = "Yorum yapan")
  post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = "yorum yapılan Post")
  comment = models.TextField(max_length = 200, verbose_name = "Yorum")
  created_at = models.DateTimeField(auto_now_add = True, verbose_name = "Yorum yapılan Tarih")
  
  def __str__(self):
    return self.owner.name

  class Meta:
    verbose_name_plural = "Yorumlar"
    verbose_name = "Yorum"
    ordering = ['-created_at']
    

class Notificate(models.Model):
  ACTIONS = (
    ('begeni', 'Beğenme'),
    ('retweet', 'Retweet'),
    ('kaydetme', 'Kaydetme'),
    ('takip', 'Takip'),
    ('yorum', 'Yorum')
  )
  receiver = models.ForeignKey('user.Profile', on_delete = models.CASCADE, verbose_name = "Bildirim Alan")
  sender = models.ForeignKey('user.Profile', on_delete = models.CASCADE, verbose_name = "Bildirim Gönderen", related_name = "send")
  post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = "İşlem yapılan Post", null = True)
  action = models.CharField(max_length=50, choices = ACTIONS, verbose_name = "İşlem")
  message = models.TextField(blank=True, null = True, verbose_name = "İşlem Mesajı")
  isRead = models.BooleanField(default = False, verbose_name = "Okundu Bilgisi")
  created_at = models.DateTimeField(auto_now_add = True, null = True)
  def __str__(self):
    return self.receiver.name + " " + self.action
  
  class Meta:
    verbose_name_plural = "Bildirimler"
    verbose_name = "Bildirim"
    
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    count = Notificate.objects.filter(receiver = self.receiver, isRead = False).count()
    print(count)
    if count == 5 or count == 10:
      print("Çalıştı")
      subject = "Yeni Bildirimleriniz var"
      message = "Kullanıcılar sizin hesabınızla etkileşime girdiler. Bildirimlerinizi kontrol edin"
      send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [self.receiver.user.email],
        fail_silently=False
      )
    