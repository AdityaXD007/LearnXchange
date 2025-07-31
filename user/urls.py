from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/remove/<int:skill_id>/', views.remove_skill, name='remove_skill'),
    path('skills/update-status/', views.update_skill_status, name='update_skill_status'),
    path('skills/update-sessions/', views.update_sessions_count, name='update_sessions_count'),
    path('skills/create-custom/', views.create_custom_skill, name='create_custom_skill'),
    
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.password_reset_request, name='password_reset'),
    path('forgot-password/otp/', views.password_reset_otp, name='password_reset_otp'),
    path('forgot-password/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
