from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, Group
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from tracksheet.forms import RegistrationForm
from django.http import HttpResponse, HttpResponseRedirect,request
import re


def index(request):

    if '_auth_user_id' in request.session:
        return redirect('/tracksheet/')
    else:
        return render(request,'tracksheet/hometheme.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            g = Group.objects.get(name='Labeller')
            g.user_set.add(user)
            auth.login(request, user)
            message = "Thank you for register with TrackerPRO,Kindly Login with your username and password."
            return redirect('/accounts/login')
    else:
        form = RegistrationForm()
    return render(request,'registration/register.html', {'form' : form})

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")



#Use Pip ==== pip install -r requirement.txt