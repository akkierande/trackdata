# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin import AdminSite
from .models import Project, Package, Image, Employee, Checkout





from import_export import resources,widgets, fields


# Register your models here.

class ImageResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project',
                           widget=widgets.ForeignKeyWidget(Project, 'project_name'))
    package = fields.Field(column_name='package', attribute='package',
                           widget=widgets.ForeignKeyWidget(Package, 'package_name'))
    class Meta:
        model = Image
        fields = ('id','image_name', 'image_type', 'status', 'project', 'package', 'file_type', 'created_at')
        export_order = ('id','image_name', 'image_type', 'status', 'project', 'package', 'file_type', 'created_at')


from import_export.admin import ImportExportModelAdmin


class ImageAdmin(ImportExportModelAdmin):
    if Checkout.image_status == "labelled":
        labelled_image =  Checkout.image_name
    resource_class = ImageResource
    list_display = ('image_name', 'image_type','status','project', 'package','file_type','created_at')
    search_fields = ('image_name','package','status')
    list_per_page = 10





class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','customer','project_type','start_date','end_date','resources','total_packages','current_uploaded','challenges','project_status','created_at')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'total_image', 'project', 'package_status','package_date','completed_date','uploaded_date','created_at')
    search_fields = ('package_name', 'package_status')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user','fullname','dob','department','previous_designation','designation','shift','emp_id','project','education','location','experience','created_at')


class CheckoutAdmin(ImportExportModelAdmin):
    list_display = ('image_name','image_objects','image_status','checkin_at','checkout_at','created_by','created_at','comment','total_time')
    search_fields = ('image_name', 'image_status')







admin.site.register(Project,ProjectAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Checkout, CheckoutAdmin)
