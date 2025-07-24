from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default-avatar.png', blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    languages = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0.0)
    sessions = models.IntegerField(default=0)
    skills = models.IntegerField(default=0)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    