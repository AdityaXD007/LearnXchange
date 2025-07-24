from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.password_reset_request, name='password_reset'),
    path('forgot-password/otp/', views.password_reset_otp, name='password_reset_otp'),
    path('forgot-password/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
