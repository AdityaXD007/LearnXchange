from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def dashboard(request):
    return render(request, 'home/dashboard.html')

def matching(request):
    return render(request, 'home/matching.html')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Check if the image file actually exists
    if profile.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(profile.image))
        if not os.path.exists(image_path):
            # Clear the broken image reference
            profile.image = None
            profile.save()
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            profile.image = image
            profile.save()
        return redirect('profile')

    return render(request, 'home/profile.html', {
        'user': request.user,
        'profile': profile
    })

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

        return redirect('profile')  # replace with your URL name if different

    return redirect('profile')

def sessions(request):
    return render(request, 'home/sessions.html')

def calendar(request):
    return render(request, 'home/calendar.html')

def base(request):
    return render(request, 'base/base.html')

def navbar(request):
    return render(request, 'base/navbar.html')

def footer(request):
    return render(request, 'base/footer.html')  


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
    return render(request, 'home/login.html', {'next': next_url})

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
    
    return render(request, 'home/signup.html', {'form': form})

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

