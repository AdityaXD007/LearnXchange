from django.contrib import admin
from .models import SEO

# Register your models here.

@admin.register(SEO)    
class SEOAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'title', 'description', 'keywords')