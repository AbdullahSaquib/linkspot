from django.shortcuts import render, redirect
from catlin.models import UserProfile
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            UserProfile(user=form.save()).save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for '+username+'!')
            return redirect('catlin:index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html', {})
