from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from tracksheet.forms import RegistrationForm
from django.http import HttpResponse, HttpResponseRedirect,request


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
            auth.login(request, user)
            return redirect('/accounts/login')
    else:
        form = RegistrationForm()
        return render(request,'registration/register.html', {'form' : form})




#Use Pip ==== pip install -r requirement.txt