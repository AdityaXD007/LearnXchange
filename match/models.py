
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from user.models import Skill, UserSkill, Profile

class SessionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('cancelled', 'Cancelled'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    skill_to_learn = models.CharField(max_length=100)
    skill_to_teach = models.CharField(max_length=100)
    session_length = models.PositiveIntegerField()  # in minutes
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.requester.username} -> {self.partner.username} ({self.status})"


class LearningSession(models.Model):
    SESSION_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    request = models.OneToOneField(SessionRequest, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_sessions')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_sessions')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    duration = models.PositiveIntegerField()  # in minutes
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='scheduled')
    notes = models.TextField(blank=True)
    rating_by_student = models.PositiveIntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    rating_by_teacher = models.PositiveIntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    feedback_by_student = models.TextField(blank=True)
    feedback_by_teacher = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_time']
    
    def __str__(self):
        return f"{self.student.username} learning {self.skill.name} from {self.teacher.username}"


class UserActivity(models.Model):
    """Track user online status and activity"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"


# Additional views for handling session requests

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

@login_required
@require_POST
def request_session(request):
    """Handle session request creation"""
    partner_username = request.POST.get('partner_username')
    skill_to_learn = request.POST.get('skill_to_learn')
    skill_to_teach = request.POST.get('skill_to_teach')
    session_length = request.POST.get('session_length')
    message = request.POST.get('message', '')
    
    try:
        partner = User.objects.get(username=partner_username)
        
        # Check if request already exists
        existing_request = SessionRequest.objects.filter(
            requester=request.user,
            partner=partner,
            status='pending'
        ).first()
        
        if existing_request:
            messages.warning(request, f'You already have a pending request with {partner.username}')
        else:
            # Create new session request
            session_request = SessionRequest.objects.create(
                requester=request.user,
                partner=partner,
                skill_to_learn=skill_to_learn,
                skill_to_teach=skill_to_teach,
                session_length=int(session_length),
                message=message
            )
            messages.success(request, f'Session request sent to {partner.username}!')
    
    except User.DoesNotExist:
        messages.error(request, 'User not found')
    except Exception as e:
        messages.error(request, 'Something went wrong. Please try again.')
    
    return redirect('matching')


@login_required
def session_requests_view(request):
    """Display session requests (sent and received)"""
    sent_requests = SessionRequest.objects.filter(requester=request.user).select_related(
        'partner', 'partner__profile'
    )
    received_requests = SessionRequest.objects.filter(partner=request.user).select_related(
        'requester', 'requester__profile'
    )
    
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    
    return render(request, 'session_requests.html', context)


@login_required
@require_POST
def handle_session_request(request, request_id):
    """Handle accepting/declining session requests"""
    session_request = get_object_or_404(SessionRequest, id=request_id, partner=request.user)
    action = request.POST.get('action')
    
    if action == 'accept':
        session_request.status = 'accepted'
        session_request.save()
        messages.success(request, f'Session request from {session_request.requester.username} accepted!')
        
        # Optional: Create a LearningSession object here or redirect to scheduling
        # You can add scheduling functionality later
        
    elif action == 'decline':
        session_request.status = 'declined'
        session_request.save()
        messages.info(request, f'Session request from {session_request.requester.username} declined.')
    
    return redirect('session_requests')


@login_required
def user_profile_view(request, username):
    """View user profile with their skills"""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    teaching_skills = UserSkill.objects.filter(
        user=user, skill_type='teaching'
    ).select_related('skill')
    
    learning_skills = UserSkill.objects.filter(
        user=user, skill_type='learning'
    ).select_related('skill')
    
    # Get recent sessions for reviews
    recent_sessions = LearningSession.objects.filter(
        Q(teacher=user) | Q(student=user),
        status='completed',
        rating_by_student__isnull=False
    ).select_related('student', 'teacher', 'skill')[:5]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'teaching_skills': teaching_skills,
        'learning_skills': learning_skills,
        'recent_sessions': recent_sessions,
        'is_own_profile': user == request.user,
    }
    
    return render(request, 'user_profile.html', context)


# Utility functions

def update_user_ratings():
    """Update user ratings based on session feedback"""
    from django.db.models import Avg
    
    for profile in Profile.objects.all():
        # Calculate average rating from teaching sessions
        avg_rating = LearningSession.objects.filter(
            teacher=profile.user,
            rating_by_student__isnull=False
        ).aggregate(avg_rating=Avg('rating_by_student'))['avg_rating']
        
        if avg_rating:
            profile.rating = round(avg_rating, 1)
            profile.save()


def update_session_counts():
    """Update session counts for users"""
    for profile in Profile.objects.all():
        # Count completed sessions (both teaching and learning)
        teaching_sessions = LearningSession.objects.filter(
            teacher=profile.user,
            status='completed'
        ).count()
        
        learning_sessions = LearningSession.objects.filter(
            student=profile.user,
            status='completed'
        ).count()
        
        profile.sessions = teaching_sessions + learning_sessions
        profile.save()


def update_user_activity(user):
    """Update user activity status"""
    activity, created = UserActivity.objects.get_or_create(user=user)
    activity.last_activity = timezone.now()
    activity.is_online = True
    activity.save()


# Middleware to track user activity (optional)
class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            update_user_activity(request.user)
        
        response = self.get_response(request)
        return response


# Management command to update ratings and session counts
# Create file: management/commands/update_user_stats.py

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Update user ratings and session counts'
    
    def handle(self, *args, **options):
        self.stdout.write('Updating user ratings...')
        update_user_ratings()
        
        self.stdout.write('Updating session counts...')
        update_session_counts()
        
        self.stdout.write(self.style.SUCCESS('Successfully updated user stats'))


# Signals to automatically update stats
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=LearningSession)
def update_profile_stats(sender, instance, **kwargs):
    """Update profile stats when a session is completed"""
    if instance.status == 'completed' and instance.rating_by_student:
        # Update teacher's rating
        avg_rating = LearningSession.objects.filter(
            teacher=instance.teacher,
            rating_by_student__isnull=False
        ).aggregate(avg_rating=models.Avg('rating_by_student'))['avg_rating']
        
        if avg_rating:
            profile = instance.teacher.profile
            profile.rating = round(avg_rating, 1)
            profile.save()
        
        # Update session counts for both users
        for user in [instance.teacher, instance.student]:
            session_count = LearningSession.objects.filter(
                models.Q(teacher=user) | models.Q(student=user),
                status='completed'
            ).count()
            
            profile = user.profile
            profile.sessions = session_count
            profile.save()