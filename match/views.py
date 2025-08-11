from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def matching(request):
    return render(request, 'home/matching.html')
