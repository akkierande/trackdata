#myproject/myproject/templatetags/tags.py

from django import template
from tracksheet.models import User,Image,Employee,Package
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag
def number_of_users(request):
    total_count = User.objects.count()
    return total_count


@register.simple_tag
def number_of_images(request):
    total_images = Image.objects.count()
    return total_images

@register.simple_tag
def number_of_visitor(request):
    uniq_visitor = Employee.objects.count()
    return uniq_visitor

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

