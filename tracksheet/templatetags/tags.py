#myproject/myproject/templatetags/tags.py

from django import template
from tracksheet.models import User,Image,Employee

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