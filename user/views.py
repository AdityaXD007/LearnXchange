from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import os
from django.conf import settings
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .models import UserSkill, Skill
import random

# Create your views here.

@login_required
def profile(request):
    # --- Original profile logic ---
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    
    # Check for broken image
    if profile_obj.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(profile_obj.image))
        if not os.path.exists(image_path):
            profile_obj.image = None
            profile_obj.save()
    
    # Handle image upload (POST)
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            profile_obj.image = image
            profile_obj.save()
        return redirect('profile')

    # --- New skills logic ---
    teaching_skills = UserSkill.objects.filter(
        user=request.user, 
        skill_type='teaching'
    ).select_related('skill')
    
    learning_skills = UserSkill.objects.filter(
        user=request.user, 
        skill_type='learning'
    ).select_related('skill')
    
    all_skills = Skill.objects.all().order_by('name')

    # Combined context
    context = {
        'user': request.user,
        'profile': profile_obj,
        'teaching_skills': teaching_skills,
        'learning_skills': learning_skills,
        'all_skills': all_skills,
    }
    return render(request, 'home/profile.html', context)

@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)

        profile.full_name = request.POST.get('full_name')
        profile.email = request.POST.get('email')
        profile.location = request.POST.get('location')
        profile.bio = request.POST.get('bio')
        profile.languages = request.POST.get('languages')
        profile.save()

        return redirect('profile')

    return redirect('profile')


@login_required
def add_skill(request):
    """Add a new skill to user's profile"""
    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        skill_type = request.POST.get('skill_type')
        proficiency_level = request.POST.get('proficiency_level')
        status = request.POST.get('status', 'new')
        
        # Check if skill exists
        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            messages.error(request, 'Selected skill does not exist.')
            return redirect('profile')
        
        # Check if user already has this skill with same type
        if UserSkill.objects.filter(user=request.user, skill=skill, skill_type=skill_type).exists():
            messages.error(request, f'You already have {skill.name} in your {skill_type} skills.')
            return redirect('profile')
        
        # Create new user skill
        UserSkill.objects.create(
            user=request.user,
            skill=skill,
            skill_type=skill_type,
            proficiency_level=proficiency_level,
            status=status
        )
        
        messages.success(request, f'{skill.name} added to your {skill_type} skills!')
        return redirect('profile')
    
    return redirect('profile')

@login_required
def remove_skill(request, skill_id):
    """Remove a skill from user's profile"""
    if request.method == 'POST':
        user_skill = get_object_or_404(UserSkill, id=skill_id, user=request.user)
        skill_name = user_skill.skill.name
        user_skill.delete()
        messages.success(request, f'{skill_name} removed from your skills.')
    
    return redirect('profile')

@login_required
@csrf_exempt
def update_skill_status(request):
    """Update skill status via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        skill_id = data.get('skill_id')
        new_status = data.get('status')
        
        try:
            user_skill = UserSkill.objects.get(id=skill_id, user=request.user)
            user_skill.status = new_status
            user_skill.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Status updated successfully',
                'new_status_color': user_skill.get_status_color()
            })
        except UserSkill.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Skill not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
@csrf_exempt
def update_sessions_count(request):
    """Update sessions count via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        skill_id = data.get('skill_id')
        increment = data.get('increment', 1)
        
        try:
            user_skill = UserSkill.objects.get(id=skill_id, user=request.user)
            user_skill.sessions_count += increment
            if user_skill.sessions_count < 0:
                user_skill.sessions_count = 0
            user_skill.save()
            
            return JsonResponse({
                'success': True,
                'new_count': user_skill.sessions_count,
                'sessions_text': user_skill.get_sessions_text()
            })
        except UserSkill.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Skill not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def create_custom_skill(request):
    """Create a custom skill if it doesn't exist"""
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name', '').strip()
        skill_type = request.POST.get('skill_type')
        proficiency_level = request.POST.get('proficiency_level')
        icon_class = request.POST.get('icon_class', 'fas fa-code')
        color_class = request.POST.get('color_class', 'text-blue-500')
        
        if not skill_name:
            messages.error(request, 'Skill name is required.')
            return redirect('profile')
        
        # Get or create the skill
        skill, created = Skill.objects.get_or_create(
            name__iexact=skill_name,
            defaults={
                'name': skill_name,
                'icon_class': icon_class,
                'color_class': color_class,
                'category': 'other'
            }
        )
        
        # Check if user already has this skill with same type
        if UserSkill.objects.filter(user=request.user, skill=skill, skill_type=skill_type).exists():
            messages.error(request, f'You already have {skill.name} in your {skill_type} skills.')
            return redirect('profile')
        
        # Create user skill
        UserSkill.objects.create(
            user=request.user,
            skill=skill,
            skill_type=skill_type,
            proficiency_level=proficiency_level,
            status='new'
        )
        
        if created:
            messages.success(request, f'New skill "{skill.name}" created and added to your profile!')
        else:
            messages.success(request, f'{skill.name} added to your {skill_type} skills!')
        
        return redirect('profile')
    
    return redirect('profile')



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next') or 'index'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    # Handle GET request
    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'next': next_url})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('index')
        else:
            # Debug: Print what errors are occurring
            print("Form is not valid!")
            print("Form errors:", form.errors)
            print("Form data:", request.POST)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)  # logs out on both GET and POST
    return redirect('index')



def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))  # 6-digit OTP
            request.session['reset_email'] = email
            request.session['otp'] = otp
            
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            return redirect('password_reset_otp')
        except User.DoesNotExist:
            return render(request, 'reset_password/password_reset.html', {'error': 'User not found'})
    return render(request, 'reset_password/password_reset.html')

def password_reset_otp(request):
    if request.method == "POST":
        if request.POST['otp'] == request.session.get('otp'):
            return redirect('password_reset_confirm')
        return render(request, 'reset_password/password_reset_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'reset_password/password_reset_otp.html')

def password_reset_confirm(request):
    if request.method == "POST":
        password = request.POST['password']
        email = request.session.get('reset_email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            request.session.flush()
            return render(request, 'reset_password/password_reset_complete.html')
        except:
            return redirect('password_reset')
    return render(request, 'reset_password/password_reset_confirm.html')


