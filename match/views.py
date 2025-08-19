# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Profile, Skill, UserSkill, SessionRequest

@login_required
def matching_view(request):
    current_user = request.user
    
    # Get current user's skills
    user_teaching_skills = UserSkill.objects.filter(
        user=current_user, 
        skill_type='teaching'
    ).values_list('skill__name', flat=True)
    
    user_learning_skills = UserSkill.objects.filter(
        user=current_user, 
        skill_type='learning'
    ).values_list('skill__name', flat=True)
    
    # Get filters from request
    search_query = request.GET.get('search', '').strip()
    skill_filter = request.GET.get('skill_filter', '')
    level_filter = request.GET.get('level_filter', '')
    availability_filter = request.GET.get('availability', '')
    rating_filter = request.GET.get('rating', '')
    session_type_filter = request.GET.get('session_type', '')
    sort_by = request.GET.get('sort', 'relevance')
    
    # Find potential matches
    potential_matches = User.objects.exclude(id=current_user.id).filter(
        profile__isnull=False
    ).select_related('profile').prefetch_related(
        'user_skills__skill'
    )
    
    # Apply search filter
    if search_query:
        potential_matches = potential_matches.filter(
            Q(profile__full_name__icontains=search_query) |
            Q(user_skills__skill__name__icontains=search_query) |
            Q(profile__bio__icontains=search_query)
        ).distinct()
    
    # Apply skill filter
    if skill_filter:
        potential_matches = potential_matches.filter(
            user_skills__skill__name__iexact=skill_filter
        ).distinct()
    
    # Apply level filter
    if level_filter:
        potential_matches = potential_matches.filter(
            user_skills__proficiency_level=level_filter
        ).distinct()
    
    # Apply rating filter
    if rating_filter:
        min_rating = float(rating_filter)
        potential_matches = potential_matches.filter(
            profile__rating__gte=min_rating
        )
    
    # Calculate match data for each potential match
    matches_with_scores = []
    for user in potential_matches:
        match_data = calculate_match_score(current_user, user)
        if match_data['score'] > 0:  # Only include users with some match
            matches_with_scores.append(match_data)
    
    # Sort matches
    if sort_by == 'rating':
        matches_with_scores.sort(key=lambda x: x['user'].profile.rating, reverse=True)
    elif sort_by == 'sessions':
        matches_with_scores.sort(key=lambda x: x['user'].profile.sessions, reverse=True)
    elif sort_by == 'recent':
        matches_with_scores.sort(key=lambda x: x['user'].last_login or x['user'].date_joined, reverse=True)
    else:  # relevance (default)
        matches_with_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Get statistics
    total_matches = len(matches_with_scores)
    perfect_matches = len([m for m in matches_with_scores if m['score'] >= 90])
    online_now = len([m for m in matches_with_scores if is_user_online(m['user'])])
    
    # Get popular skills
    popular_skills = Skill.objects.annotate(
        user_count=Count('userskill')
    ).order_by('-user_count')[:4]
    
    # Get all available skills for filter dropdown
    all_skills = Skill.objects.all().order_by('name')
    
    context = {
        'matches': matches_with_scores,
        'total_matches': total_matches,
        'perfect_matches': perfect_matches,
        'online_now': online_now,
        'popular_skills': popular_skills,
        'all_skills': all_skills,
        'search_query': search_query,
        'skill_filter': skill_filter,
        'level_filter': level_filter,
        'sort_by': sort_by,
        'current_user_teaching': list(user_teaching_skills),
        'current_user_learning': list(user_learning_skills),
    }
    
    return render(request, 'home/matching.html', context)


def calculate_match_score(current_user, other_user):
    """Calculate match score between two users based on complementary skills"""
    score = 0
    perfect_match = False
    
    # Get current user's skills
    current_teaching = set(UserSkill.objects.filter(
        user=current_user, skill_type='teaching'
    ).values_list('skill__name', flat=True))
    
    current_learning = set(UserSkill.objects.filter(
        user=current_user, skill_type='learning'
    ).values_list('skill__name', flat=True))
    
    # Get other user's skills
    other_teaching = set(UserSkill.objects.filter(
        user=other_user, skill_type='teaching'
    ).values_list('skill__name', flat=True))
    
    other_learning = set(UserSkill.objects.filter(
        user=other_user, skill_type='learning'
    ).values_list('skill__name', flat=True))
    
    # Perfect match: they teach what we want to learn AND want to learn what we teach
    mutual_skills_1 = current_learning.intersection(other_teaching)
    mutual_skills_2 = current_teaching.intersection(other_learning)
    
    if mutual_skills_1 and mutual_skills_2:
        perfect_match = True
        score = 95
    elif mutual_skills_1 or mutual_skills_2:
        # Good match: one-way skill exchange
        score = 75 + len(mutual_skills_1 | mutual_skills_2) * 5
    else:
        # Basic compatibility based on skill categories or general interest
        score = 30
    
    # Bonus points for high rating
    if hasattr(other_user, 'profile') and other_user.profile.rating >= 4.5:
        score += 10
    elif hasattr(other_user, 'profile') and other_user.profile.rating >= 4.0:
        score += 5
    
    # Get user's teaching and learning skills for display
    other_user_teaching = UserSkill.objects.filter(
        user=other_user, skill_type='teaching'
    ).select_related('skill')
    
    other_user_learning = UserSkill.objects.filter(
        user=other_user, skill_type='learning'
    ).select_related('skill')
    
    return {
        'user': other_user,
        'score': min(score, 100),  # Cap at 100%
        'perfect_match': perfect_match,
        'teaching_skills': other_user_teaching,
        'learning_skills': other_user_learning,
        'mutual_teaching': mutual_skills_1,
        'mutual_learning': mutual_skills_2,
        'is_online': is_user_online(other_user),
    }


def is_user_online(user):
    """Check if user is currently online (you'll need to implement this based on your online tracking)"""
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Simple check based on last_login (you might want to implement a more sophisticated system)
    if user.last_login:
        return user.last_login > timezone.now() - timedelta(minutes=30)
    return False


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
    except ValueError:
        messages.error(request, 'Invalid session length')
    except Exception as e:
        messages.error(request, 'Something went wrong. Please try again.')
    
    return redirect('matching')


@login_required
def session_requests_view(request):
    """Display session requests (sent and received)"""
    sent_requests = SessionRequest.objects.filter(
        requester=request.user
    ).select_related('partner', 'partner__profile').order_by('-created_at')
    
    received_requests = SessionRequest.objects.filter(
        partner=request.user
    ).select_related('requester', 'requester__profile').order_by('-created_at')
    
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    
    return render(request, 'session_requests.html', context)


@login_required
@require_POST
def handle_session_request(request, request_id):
    """Handle accepting/declining session requests"""
    session_request = get_object_or_404(
        SessionRequest, 
        id=request_id, 
        partner=request.user,
        status='pending'  # Only allow handling pending requests
    )
    
    action = request.POST.get('action')
    
    if action == 'accept':
        session_request.status = 'accepted'
        session_request.save()
        messages.success(
            request, 
            f'Session request from {session_request.requester.username} accepted!'
        )
        
    elif action == 'decline':
        session_request.status = 'declined'
        session_request.save()
        messages.info(
            request, 
            f'Session request from {session_request.requester.username} declined.'
        )
    else:
        messages.error(request, 'Invalid action')
    
    return redirect('session_requests')


@login_required
def user_profile_view(request, username):
    """View user profile with their skills"""
    user = get_object_or_404(User, username=username)
    
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'User profile not found')
        return redirect('matching')
    
    teaching_skills = UserSkill.objects.filter(
        user=user, skill_type='teaching'
    ).select_related('skill')
    
    learning_skills = UserSkill.objects.filter(
        user=user, skill_type='learning'
    ).select_related('skill')
    
    context = {
        'profile_user': user,
        'profile': profile,
        'teaching_skills': teaching_skills,
        'learning_skills': learning_skills,
        'is_own_profile': user == request.user,
    }
    
    return render(request, 'user_profile.html', context)