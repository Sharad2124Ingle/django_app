from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def home(request):
    # Check if user is authenticated before filtering records
    if request.user.is_authenticated:
        records = Record.objects.all
    else:
        records = None

    return render(request, 'home.html', {'records': records})

def login_user(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if the user is active and not anonymous
                if user.is_active and not user.is_anonymous:
                    login(request, user)
                    messages.success(request, "Welcome!")
                    return redirect('home')
                else:
                    messages.error(request, "Your account is not active.")
            else:
                messages.error(request, "Invalid credentials. Please try again or sign up.")
        else:
            messages.error(request, "Invalid credentials. Please try again or sign up.")
            return redirect('home')

    return render(request, 'loginpage.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login_page')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            messages.success(request, "account created, please login.")
            return redirect('login_page')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})

@login_required
def add_record(request):
    messages.success(request, "you can add a record below")

    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            # Get the logged-in user and set it as the user of the record
            form.instance.user = request.user
            form.save()
            return redirect('home')
    else:
        form = AddRecordForm()

    return render(request, 'add_record.html', {'form': form})




