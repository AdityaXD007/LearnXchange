from django.contrib import admin
from .models import Profile, SEO

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'location') 

@admin.register(SEO)    
class SEOAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'title', 'description', 'keywords')