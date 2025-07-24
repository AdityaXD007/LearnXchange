from django.db import models
from django.contrib.auth.models import User


class SEO(models.Model):
    page_name = models.CharField(max_length=100, unique=True)  # like 'about', 'index', etc.
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    

    def __str__(self):
        return self.page_name