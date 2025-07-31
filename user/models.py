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


class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('language', 'Language'),
        ('photography', 'Photography'),
        ('music', 'Music'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, default='other')
    icon_class = models.CharField(max_length=50, help_text="FontAwesome icon class")
    color_class = models.CharField(max_length=50, help_text="Tailwind color class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserSkill(models.Model):
    SKILL_TYPES = [
        ('teaching', 'Teaching'),
        ('learning', 'Learning'),
    ]
    
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('learning', 'Learning'),
        ('in_progress', 'In Progress'),
        ('new', 'New'),
        ('paused', 'Paused'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPES)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    sessions_count = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'skill', 'skill_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.skill_type})"
    
    def get_status_color(self):
        status_colors = {
            'active': 'bg-green-100 text-green-800',
            'learning': 'bg-blue-100 text-blue-800',
            'in_progress': 'bg-yellow-100 text-yellow-800',
            'new': 'bg-gray-100 text-gray-800',
            'paused': 'bg-red-100 text-red-800',
        }
        return status_colors.get(self.status, 'bg-gray-100 text-gray-800')
    
    def get_sessions_text(self):
        if self.skill_type == 'teaching':
            return f"{self.sessions_count} sessions taught"
        else:
            if self.sessions_count == 0:
                return "Just started"
            return f"{self.sessions_count} sessions completed"
    