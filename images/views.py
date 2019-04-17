from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.http import HttpResponseRedirect
from django.shortcuts import render

from images.forms import SignUpForm
from images.forms import LoginForm
from mixpanel import Mixpanel
import datetime
mp = Mixpanel('bc31cfd87d35ef238a0215c0d2278745')


def index(request):
    """Return the logged in page, or the logged out page
    """
    if request.user.is_authenticated():
        return render(request, 'images/index-logged-in.html', {
            'user': request.user
        })
    else:
        return render(request, 'images/index-logged-out.html')



def signup(request):
    """Render the Signup form or a process a signup
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            mp.track(username, 'New Sign Up', {
                'Username': username,
                'Signup Date': datetime.datetime.now()
            })
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            log_in(request, user)
            return HttpResponseRedirect('/')
        
            

    else:
        form = SignUpForm()
        

    return render(request, 'images/signup.html', {'form': form})


def save_profile(request):
    profile = Profile.objects.get(email=request.user.email)
    distinct_id = form.cleaned_data.get('distinct_id')
    profile.distinct_id = distinct_id
    profile.save()
  

def login(request):
    """Render the login form or log in the user
    """
    if request.method == 'POST':
        username = request.POST['username']
        mp.track(username, 'Returning User')
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            log_in(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'images/login.html', {
                'form': LoginForm,
                'error': 'Please try again'
            })
    else:
        return render(request, 'images/login.html', {'form': LoginForm})



def logout(request):
    """Logout the user
    """
    mp.track(logout, 'Logout')
    log_out(request)
    return HttpResponseRedirect('/')
    


     