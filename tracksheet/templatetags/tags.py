#myproject/myproject/templatetags/tags.py
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django import template
from tracksheet.models import User,Image,Employee,Package,Project,Checkout
from django.contrib.auth.models import Group
from django.db.models import Count
from datetime import datetime
from django.db.models import Q

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
##########################################################

@register.simple_tag
def current_month(request):
    current_month = datetime.now().strftime('%B')
    return current_month

##########################################################


@register.simple_tag
def number_of_users(request):
    total_count = User.objects.count()
    return total_count

@register.simple_tag
def number_of_users_current_month(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    new = Employee.objects.filter(created_at__month=current_month,created_at__year = current_year)
    total_users_month = new.count()
    return total_users_month

#####################################################

@register.simple_tag
def number_of_checkouts(request):
    total_checkouts = Checkout.objects.count()
    return total_checkouts

@register.simple_tag
def number_of_checkouts_current_month(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    new = Checkout.objects.filter(created_at__month=current_month,created_at__year = current_year)
    total_checkouts = new.count()
    return total_checkouts

@register.simple_tag
def number_of_checkout_user(request):
    new = Checkout.objects.filter(created_by = request.user)
    total_checkout_user = new.count()
    return total_checkout_user

@register.simple_tag
def number_of_checkout_user_approved(request):
    new = Checkout.objects.filter(created_by = request.user,image_status = "Approved")
    total_checkout_user_approved = new.count()
    return total_checkout_user_approved

@register.simple_tag
def number_of_checkout_current_month_user(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    new = Checkout.objects.filter(created_at__month=current_month,created_at__year = current_year,created_by = request.user)
    total_checkout_current_month_user = new.count()
    return total_checkout_current_month_user

@register.simple_tag
def number_of_checkout_current_month_user_approved(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    new = Checkout.objects.filter(created_at__month=current_month,created_at__year = current_year,created_by = request.user,image_status = "Approved")
    total_checkout_month_user_approved = new.count()
    return total_checkout_month_user_approved

#####################################################

@register.simple_tag
def number_of_images(request):
    total_images = Image.objects.count()
    return total_images

@register.simple_tag
def number_of_images_current_month(request):
    #total_checkouts = Checkout.objects.count()
    current_month = datetime.now().month
    current_year = datetime.now().year
    new = Image.objects.filter(created_at__month=current_month,created_at__year = current_year)
    total_images_month = new.count()
    # current_month = datetime.now().month
    # Checkout.ordering.objects.filter(created_at__month=current_month)
    return total_images_month

@register.simple_tag
def number_of_images_user(request):
    new = Image.objects.filter( assign_to = request.user)
    total_images_user = new.count()
    return total_images_user

@register.simple_tag
def number_of_images_user_labelled(request):
    new = Image.objects.filter( label_by = request.user)
    total_images_user_labelled = new.count()
    return total_images_user_labelled

@register.simple_tag
def number_of_images_current_month_user(request):
    #total_checkouts = Checkout.objects.count()
    current_month = datetime.now().month
    current_year = datetime.now().year
    new = Image.objects.filter(created_at__month=current_month,created_at__year = current_year,label_by = request.user).distinct()
    total_images_month_user = new.count()
    # current_month = datetime.now().month
    # Checkout.ordering.objects.filter(created_at__month=current_month)
    return total_images_month_user

@register.simple_tag
def checkout_is_null(checkout_id):
    qs = Checkout.objects.filter(checkout_id == Checkout.pk)
    if qs.checkin_at == "":
        return True

@register.simple_tag
def image_project_check(request,image_id):
    qs = Image.objects.filter(project.project_name == image_id)
    if qs.checkin_at == "":
        return True

####################################################################


#Q(question__startswith='Who') | Q(question__startswith='What')




@register.simple_tag
def number_of_labelled(request):
    total_labelled = Image.objects.filter(Q(status = "Labelled")|
                                          Q(status="Approved") |
                                          Q(status="Corrected")|
                                          Q(status="ChangeNeeded")|
                                          Q(status="InQuality")|
                                          Q(status="Uploaded")).count()
    return total_labelled

@register.simple_tag
def box_images(request):
    total_box = Image.objects.filter(project__project_name = "Box Labelling").count()
    return total_box

@register.simple_tag
def image_piechart(request,pk):
    unlabelled = Image.objects.filter(status="Unlabelled",project__id = pk).count()
    labelled = Image.objects.filter(status="Labelled",project__id = pk).count()
    inprocess = Image.objects.filter(status="InProcess",project__id = pk).count()
    corrected = Image.objects.filter(status="Corrected",project__id = pk).count()
    changeneeded = Image.objects.filter(status="ChangeNeeded",project__id = pk).count()
    inquality = Image.objects.filter(status="InQuality",project__id = pk).count()
    approved = Image.objects.filter(status="Approved",project__id = pk).count()
    uploaded = Image.objects.filter(status="Uploaded",project__id = pk).count()
    all_data = [unlabelled,labelled,inprocess,corrected,changeneeded,inquality,approved,uploaded]
    return all_data


@register.simple_tag
def get_user(request):
    if User.is_authenticated:
        login_user = User.objects.all()
        return login_user

@register.simple_tag
def is_labeller(user):
    print("true")
    return user.groups.filter(name__in=['Labeller']).exists()
    #print("False")
    #return group in user.groups.all()

@register.simple_tag
def get_total_packages(request):
    total_packages = Package.objects.count()
    return total_packages


