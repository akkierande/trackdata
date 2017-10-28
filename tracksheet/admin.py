# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin import AdminSite
from .models import Project, Package, Image, Employee, Checkout
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ImageResource(resources.ModelResource):

    class Meta:
        model = Image

class ImageAdmin(ImportExportModelAdmin):
    if Checkout.image_status == "labelled":
        labelled_image =  Checkout.image_id

    list_display = ('image_name', 'image_type','status','project', 'package','file_type','created_at')
    search_fields = ('image_name','package','status')
    resource_class = ImageResource
    list_per_page = 10

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','customer','project_type','start_date','end_date','resources','total_image','current_uploaded','challenges','project_status','created_at')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'total_image', 'project', 'package_status','package_date','completed_date','uploaded_date','created_at')
    search_fields = ('package_name', 'package_status')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user','fullname','dob','department','previous_designation','designation','shift','emp_id','project','education','location','experience','created_at')


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('image_id','image_objects','image_status','checkin_at','checkout_at','created_by','created_at','comment','total_time')
    search_fields = ('image_id', 'image_status')


admin.site.register(Project,ProjectAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Checkout, CheckoutAdmin)



# image_id = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
# image_objects = models.IntegerField(blank=True, null=True)
# image_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
# checkin_at = models.DateField(auto_created=True, blank=True, null=True)
# checkout_at = models.DateField(auto_created=True, blank=True, null=True)
# checkout_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
# created_at = models.DateTimeField(auto_now=True)
# comment = models.CharField(max_length=100, blank=True, null=True)
# total_time = models.CharField(max_length=10,blank=True, null=True)