from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'name', 'created_at', 'slug']
  search_fields = ['name', 'user__username__icontains']
  readonly_fields = ['id','slug','created_at']
  date_hierarchy = 'created_at'
  list_per_page = 10
# Register your models here.
admin.site.register(Profile, ProfileAdmin)