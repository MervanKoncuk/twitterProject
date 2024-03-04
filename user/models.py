from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
# Create your models here.

class Profile(models.Model):
  id = models.UUIDField(primary_key = True, unique = True, db_index = True, default = uuid.uuid4, editable = False)
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  name = models.CharField(max_length = 200, verbose_name = "İsim Soyisim")
  bio =  models.TextField(("Hakkımda"), blank=True, null=True, default = "Merhaba, Ben twitter kullanıyorum.")
  follow = models.ManyToManyField('self', symmetrical=False, related_name="takip", verbose_name= "Takip edilenler", blank=True)
  follower = models.ManyToManyField('self', symmetrical=False, related_name="takipci", verbose_name= "Takipçiler", blank=True)
  image = models.ImageField(upload_to="profiles/", verbose_name="Profil Resmi")
  created_at = models.DateTimeField(auto_now_add = True)
  slug = models.SlugField(blank=True, null=True, editable = False)

  # symmetrical
  # mervan -> admin
  # admin <- mervan
  
  def save(self, *args, **kwargs):
    self.slug = slugify(self.user.username)
    super().save(*args, **kwargs)
  
  def __str__(self):      
    return self.user.username
  
  class Meta:
    verbose_name_plural = "Profiller"
    verbose_name = "Profil"
    ordering = ['-created_at']
  