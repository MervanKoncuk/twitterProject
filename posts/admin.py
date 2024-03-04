from django.contrib import admin
from .models import *
# Register your models here.


class PostAdmin(admin.ModelAdmin):
  list_display = ['owner','content','slug','created_at']
  list_filter = ['owner']
  search_fields = ['owner__name__icontains','content']
  readonly_fields = ['id','slug','created_at']
  date_hierarchy = "created_at"
  list_per_page = 15


class CommentAdmin(admin.ModelAdmin):
  list_display = ['owner', 'post', 'comment', 'created_at']
  list_filter = ['owner']
  search_fields = ['owner__name__icontains', 'post__content__icontains', 'comment']
  date_hierarchy = 'created_at'
  list_per_page = 15

class NotificateAdmin(admin.ModelAdmin):
  list_display = ['receiver', 'sender', 'post', 'action', 'isRead', 'created_at']
  search_fields = ['receiver__name__icontains', 'sender__name__icontains', 'post__content__icontains']
  list_filter = ['action']
  date_hierarchy = 'created_at'
  list_per_page = 15


admin.site.register(Post,PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notificate, NotificateAdmin)