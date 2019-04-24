from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.http import HttpResponseRedirect
from django.shortcuts import render
from images.forms import SignUpForm
from images.forms import LoginForm
from mixpanel import Mixpanel
import datetime
import urllib
import json


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

def _get_distinct_id(request):
    """Gets distinct_id from clientside cookie"""
    raw_cookie = request.COOKIES['mp_bc31cfd87d35ef238a0215c0d2278745_mixpanel']
    json_cookie = json.loads(urllib.unquote(raw_cookie).decode('utf8'))
    d_id = json_cookie['distinct_id']
    return d_id


def signup(request):
    """Render the Signup form or a process a signup
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            distinct_id = _get_distinct_id(request)
            mp.alias(username, distinct_id)
            
            mp.track(distinct_id, 'New Sign Up', {
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

  

def login(request):
    """Render the login form or log in the user
    """
    if request.method == 'POST':
        username = request.POST['username']
        mp.track(username, 'Login',{
            'Username': username
        })
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
    log_out(request)
    return HttpResponseRedirect('/')
  
    
    


     