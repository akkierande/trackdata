#myproject/myproject/templatetags/tags.py
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django import template
from tracksheet.models import User,Image,Employee,Package,Project,Checkout
from django.contrib.auth.models import Group
from django.db.models import Count

register = template.Library()

@register.simple_tag
def number_of_users(request):
    total_count = User.objects.count()
    return total_count

@register.simple_tag
def number_of_checkouts(request):
    total_checkouts = Checkout.objects.count()
    return total_checkouts

@register.simple_tag
def number_of_images(request):
    total_images = Image.objects.count()
    return total_images

@register.simple_tag
def number_of_visitor(request):
    uniq_visitor = Employee.objects.count()
    return uniq_visitor

@register.simple_tag
def number_of_labelled(request):
    total_labelled = Image.objects.filter(status = "Labelled").count()
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


