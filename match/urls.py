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
    
    #Session management
    path('sessions/', views.sessions_view, name='sessions'),
    path('sessions/request/<int:request_id>/handle/', views.handle_session_request, name='handle_session_request'),
    path('sessions/request/<int:request_id>/cancel/', views.cancel_session_request, name='cancel_session_request'),
    path('sessions/<int:session_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('sessions/<int:session_id>/skip-feedback/', views.skip_feedback, name='skip_feedback'),
    path('sessions/<int:session_id>/reschedule/', views.reschedule_session, name='reschedule_session'),
    path('sessions/<int:session_id>/prepare/', views.prepare_session, name='prepare_session'),
]
