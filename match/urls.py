from django .urls import path, include
from match import views

urlpatterns = [
     # Matching and discovery
    path('matching/', views.matching_view, name='matching'),
    
    # Session requests
    path('request-session/', views.request_session, name='request_session'),
    path('session-requests/', views.session_requests_view, name='session_requests'),
    path('handle-request/<int:request_id>/', views.handle_session_request, name='handle_session_request'),
    
    # User profiles
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
]
