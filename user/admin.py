from django.contrib import admin
from .models import Profile, Skill, UserSkill

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'location') 

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon_class', 'color_class', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'skill_type', 'proficiency_level', 'status', 'sessions_count', 'created_at']
    list_filter = ['skill_type', 'proficiency_level', 'status', 'created_at']
    search_fields = ['user__username', 'skill__name']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'skill')    