from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('base/', views.base, name='base'),
    path('navbar/', views.navbar, name='navbar'),
    path('footer/', views.footer, name='footer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)