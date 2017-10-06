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
        fields = {
            'image_name': ['exact', 'contains'],
            #'tz': ['exact'],
        }


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
            'image_objects': ['exact', 'contains'],
            # 'tz': ['exact'],
        }
