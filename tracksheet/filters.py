import django_filters
from django_filters import FilterSet
import django_filters as filters

from .models import Package,Image,Project,Checkout
from django import forms

class ImageFilter(FilterSet):
    image_name = filters.CharFilter(label='Image -',lookup_expr='icontains')
    created_at = django_filters.DateFilter(lookup_expr='contains', widget=forms.DateInput(
        attrs={
            'class': 'datepicker',
            'type': 'date'
        }))
    class Meta:
        model = Image

        #lookup_expr = ['exact', 'iexact']
        #Image.image_name = django_filters.CharFilter(lookup_expr=['iexact'])
        #project = ['name', 'project']
        #project = Image.objects.filter(project__project_name='project')
        #project = Image.project
        #project = Image.project
        #package = Image.package
        fields = {
            'project':['exact'],
            'package': ['exact'],
            'assign_to': ['exact'],
            'set':['exact'],
            'sequence': ['exact'],
            'folder': ['exact'],
            'status': ['exact'],
            'label_by':['contains'],
        }
        # exclude = {
        #     'created_by':['exact'],
        #     'created_at': ['exact'],
        #     'updated_at': ['exact'],
        #     'updated_by': ['exact'],
        #     #'tz': ['exact'],
        # }



class ProjectFilter(FilterSet):

    empty_text = "There are no project matching the search criteria..."

    class Meta:
        model = Project
        fields = {
            'project_name': ['contains'],
            'project_status':['exact'],
            # 'tz': ['exact'],
        }

class PackageFilter(FilterSet):
    class Meta:
        model = Package
        fields = {
            'package_name': ['contains'],
            'package_date': ['exact'],
            'project': ['exact'],
            'package_status': ['contains'],
        }
#
# class PackageFilter(FilterSet):
#
#     empty_text = "There are no package matching the search criteria..."
#
#     class Meta:
#         model = Package
#         fields = {
#             'package_name': ['contains'],
#             'project': ['exact'],
#             # 'tz': ['exact'],
#         }

class CheckoutFilter(FilterSet):
    # name = Checkout.get_image_name
    # image_name = filters.CharFilter(label='Image -', lookup_expr='iexact')


    class Meta:

        model = Checkout

        fields = {
            'image_status':['exact'],
            'created_by': ['exact'],
        }

class CheckoutHistoryFilter(FilterSet):
    # name = Checkout.get_image_name

    image_name = filters.CharFilter(label='Image -', lookup_expr='iexact')
    class Meta:
        model = Checkout
        fields = {
            'image_status':['exact'],
            'created_by': ['exact'],
        }

class AssignFilter(FilterSet):
    assign_at = django_filters.DateFilter(lookup_expr='contains',widget=forms.DateInput(
        attrs = {
            'class' : 'datepicker',
            'type' : 'date'
        }))
    #empty_text = "There are no project matching the search criteria..."
    class Meta:
        model = Image
        fields = {
            'image_name': ['contains'],
            'status': ['exact'],
            'assign_at':['exact'],
        }