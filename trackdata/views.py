from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, Group
from tracksheet.models import Employee
from django.shortcuts import render,redirect,get_object_or_404
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
            instance = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')

            # f.fullname = firstname + lastname
            instance.save()
            user = authenticate(username=username, password=raw_password)
            g = Group.objects.get(name='Labeller')
            g.user_set.add(user)
            u = User.objects.get(username=username)
            f = Employee.objects.get(user=u)
            #print(u)
            #print (str(f))
            f.fullname = firstname + " " + lastname
            f.save()

            auth.login(request, user)
            message = "Thank you for register with TrackerPRO,Kindly Login with your username and password."
            return redirect('/accounts/login',{message:'message'})
    else:
        form = RegistrationForm()
    return render(request,'registration/register.html', {'form' : form})

def logout_view(request):
    auth.logout(request)



    #HttpResponseRedirect("registration/logout.html")

    # Redirect to a success page.
    return HttpResponseRedirect("/")

# from django.shortcuts import render_to_response
# from django.template import RequestContext
#
# def handler404(request):
#     response = render_to_response('404.html',{},context_instance=RequestContext(request))
#     response.status_code = 404
#     return response
#
# def handler500(request):
#     response = render_to_response('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response


#Use Pip ==== pip install -r requirement.txt