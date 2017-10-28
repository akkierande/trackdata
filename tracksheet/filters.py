import django_filters
from django_filters import FilterSet

from .models import Package,Image,Project,Checkout

class PackageFilter(FilterSet):

    class Meta:
        model = Package
        fields = {
            'package_name': ['contains'],
            'package_date': ['exact'],
            'project': ['exact'],
            'package_status': ['contains'],
        }



class ImageFilter(FilterSet):
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
            'image_name':['contains'],

        }
        # exclude = {
        #     'created_by':['exact'],
        #     'created_at': ['exact'],
        #     'updated_at': ['exact'],
        #     'updated_by': ['exact'],
        #     #'tz': ['exact'],
        # }


class ProjectFilter(FilterSet):

    empty_text = "There are no package matching the search criteria..."

    class Meta:
        model = Project
        fields = {
            'project_name': ['exact', 'contains'],
            # 'tz': ['exact'],
        }

class CheckoutFilter(FilterSet):

    class Meta:
        model = Checkout
        fields = {
            'image_id':['exact'],
            'image_status':['exact'],
            'created_by': ['exact'],
        }

class CheckoutHistoryFilter(FilterSet):

    class Meta:
        model = Checkout
        fields = {
            'image_id':['exact'],
            'image_status':['exact'],
            'created_by': ['exact'],
        }
