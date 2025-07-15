from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('matching/', views.matching, name='matching'),
    path('profile/', views.profile, name='profile'),
    path('sessions/', views.sessions, name='sessions'),
    path('calendar/', views.calendar, name='calendar'),
    path('base/', views.base, name='base'),
    path('navbar/', views.navbar, name='navbar'),
    path('footer/', views.footer, name='footer'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.password_reset_request, name='password_reset'),
    path('forgot-password/otp/', views.password_reset_otp, name='password_reset_otp'),
    path('forgot-password/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]