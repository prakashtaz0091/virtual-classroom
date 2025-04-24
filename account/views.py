from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import User, Profile


def register_view(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password') 
        confirm_password = data.get('confirm_password')
        role = data.get('role')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        
        form = CustomUserCreationForm({
            'username': username,
            'password1': password,
            'password2': confirm_password
        })
        
        if form.is_valid():
            user = User(
                username=username,
                role=role,
                first_name=firstname,
                last_name=lastname
            )
            user.set_password(password)
            user.save()
        else:
            return render(request, 'account/register.html', {'form': form})
        
        
        
        #personal info
        bio = data.get('bio')
        profile_pic = request.FILES.get('profile_pic')
        
        try:
            Profile.objects.create(
                user=user,
                bio=bio,
                avatar=profile_pic
            )
        except Exception as e:
            print(e)
            context = {'error': 'An error occurred while creating the profile.'}
            return render(request, 'account/register.html', context )   
        
        
        return redirect('login_view')
    
    return render(request, 'account/register.html')



def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        
        # check if user exists with the provided credentials
        user = authenticate(request, username=username, password=password)
        
        # if user exists, log them in
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 14 days in seconds
            else:
                request.session.set_expiry(0)  # Session expires at the end of the browser session
            return redirect('main:home')
        else:
            return render(request, 'account/login.html', {'error': 'Invalid username or password'})
        
    
   
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')