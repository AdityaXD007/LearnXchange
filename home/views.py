from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.conf import settings
from django.shortcuts import render, get_object_or_404

# Create your views here.
def dashboard(request):
    return render(request, 'home/dashboard.html')

def matching(request):
    return render(request, 'home/matching.html')

def profile(request):
    return render(request, 'home/profile.html')

def sessions(request):
    return render(request, 'sessions.html')

def calendar(request):
    return render(request, 'calendar.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    # Handle GET request
    next_url = request.GET.get('next', '')
    return render(request, 'home/login.html', {'next': next_url})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.is_staff = True  
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to homepage

    return render(request, 'home/signup.html')
def logout_view(request):
    logout(request)  # logs out on both GET and POST
    return redirect('home')


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


