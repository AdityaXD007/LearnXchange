from django .urls import path, include
from match import views

urlpatterns = [
    path('matching/', views.matching, name='matching'),
]
