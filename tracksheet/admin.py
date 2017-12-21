# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import User
from tracksheet import models
from django.http import HttpResponse
from django.contrib.admin import AdminSite
from .models import Project, Package, Image, Employee, Checkout , Set , Folder , Sequence
import bulk_admin
from import_export import resources, widgets, fields
from .filters import ImageFilter,CheckoutFilter,PackageFilter,ProjectFilter


# Register your models here.

class ImageResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project',
                           widget=widgets.ForeignKeyWidget(Project, 'project_name'))
    package = fields.Field(column_name='package', attribute='package',
                           widget=widgets.ForeignKeyWidget(Package, 'package_name'))
    folder = fields.Field(column_name='folder', attribute='folder',
                           widget=widgets.ForeignKeyWidget(Folder, 'folder_name'))
    set = fields.Field(column_name='set', attribute='set',
                          widget=widgets.ForeignKeyWidget(Set, 'set_name'))
    sequence = fields.Field(column_name='sequence', attribute='sequence',
                          widget=widgets.ForeignKeyWidget(Sequence, 'sequence_name'))


    class Meta:
        model = Image
        fields = (
        'id','project','package','sequence','folder','set','image_name', 'image_type', 'status', 'assign_to','label_time','correction_time','loop_on_image', 'file_type', 'created_at')
        export_order = (
        'id','project','package','sequence','folder','set','image_name', 'image_type', 'status', 'assign_to','label_time','correction_time','loop_on_image', 'file_type', 'created_at')


from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.helpers import ActionForm
from django import forms


class Edit1ActionForm(ActionForm):
    username = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    # username = forms.ChoiceField()


def editselected(modeladmin, request, queryset):
    assign = request.POST['username']
    rows_updated = queryset.update(assign_to=assign)
    for obj in queryset: obj.save()
    if rows_updated == 1:
        message_bit = '1 item was'
    else:
        message_bit = '%s items were' % rows_updated
    modeladmin.message_user(request, '%s successfully Updated.' % message_bit)
editselected.short_description = "Edit selected items"

## add deactivates

class ImageAdmin(ImportExportModelAdmin):
    # if Checkout.image_status == "labelled":
    #     labelled_image = Checkout.image_name
    resource_class = ImageResource
    action_form = Edit1ActionForm
    actions = [editselected]
    # inlines = [ImageInline]
    list_display = ('id','project','package','sequence','folder','set','image_name', 'image_type', 'status', 'assign_to','label_time','correction_time','loop_on_image', 'file_type', 'created_at')

    list_display_links = ('image_name','id')
    search_fields = ('image_name', 'package__package_name', 'status', 'assign_to__username')
    list_filter = ('project','package','folder','set')
    list_per_page = 20

@admin.register(models.Project)
class ProjectAdmin(bulk_admin.BulkModelAdmin):
    search_fields = ('title',)
    list_display = ('project_name', 'customer', 'project_type', 'start_date', 'end_date', 'resources', 'total_packages',
                    'current_uploaded', 'challenges', 'project_status', 'created_at')
    list_filter = ('project_name',)

@admin.register(models.Package)
class PackageAdmin(bulk_admin.BulkModelAdmin):
    list_display = ('package_name', 'total_image', 'project', 'package_status', 'package_date', 'completed_date', 'uploaded_date','created_at')
    search_fields = ('package_name', 'package_status')
    #filterset_class =
    #list_filter = PackageFilter

@admin.register(models.Sequence)
class SequenceAdmin(bulk_admin.BulkModelAdmin):
    list_display = ('total_image','sequence_name','sequence_date','project','package','sequence_status','completed_date','uploaded_date','created_at','uploaded_date','created_by','updated_by')
    search_fields = ('sequence_name', 'sequence_status')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'fullname', 'dob', 'department', 'previous_designation', 'designation', 'shift', 'emp_id', 'project',
    'education', 'location', 'experience', 'created_at')


class CheckoutAdmin(ImportExportModelAdmin):
    list_display = (
    'image_id', 'image_objects', 'image_status', 'checkin_at', 'checkout_at', 'created_by', 'created_at', 'comment',
    'total_time')
    search_fields = ('image_id', 'image_status')


#admin.site.register(Project, ProjectAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Employee, EmployeeAdmin)
#admin.site.register(Package, PackageAdmin)
admin.site.register(Set)
admin.site.register(Folder)
#admin.site.register(Sequence)
admin.site.register(Checkout, CheckoutAdmin)
