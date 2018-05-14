# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import User
from tracksheet import models
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin import AdminSite
from .models import Project, Package, Image, Employee, Checkout , Set , Folder , Sequence
import bulk_admin
from import_export import resources, widgets, fields
from .filters import ImageFilter,CheckoutFilter,PackageFilter,ProjectFilter
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model

from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.utils import timezone
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
# Register your models here.
from django.contrib.admin import DateFieldListFilter
class ImageResource(resources.ModelResource):
    User = get_user_model()
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
    # assign_to__username = fields.Field(column_name='assign_to',attribute='assign_to',widget=widgets.ForeignKeyWidget(User,'id'))

    # assign_to__username = fields.Field(
    #     column_name='assign_to__username',
    #     attribute='assign_to',
    #     widget=ForeignKeyWidget(model=User, field='username'))
    assign_to=fields.Field(column_name='assign_to',attribute='assign_to',widget=ForeignKeyWidget(model=User,field='first_name'))
    class Meta:
        model = Image
        #exclude = ('label_by',)
        fields = (
        'id','project','package','sequence','folder','set','image_name', 'image_type', 'status', 'assign_to','assign_at','label_time','label_date','correction_time','corrected_date','label_by','corrected_by','total_objects','layer_issues','border_issues','missing_objects','loop_on_image','approved_by','approved_date','remark','file_type', 'created_at','created_by')
        export_order = (
        'id','project','package','sequence','folder','set','image_name', 'image_type', 'status', 'assign_to','assign_at','label_time','label_date','correction_time','corrected_date','label_by','corrected_by','total_objects','layer_issues','border_issues','missing_objects','loop_on_image','approved_by','approved_date','remark','file_type', 'created_at','created_by')

class Edit1ActionForm(ActionForm):
    username = forms.ModelChoiceField(queryset=User.objects.order_by('username'),required=False)
    # username = forms.ChoiceField()


def editselected(modeladmin, request, queryset):
    #,assign_at = timezone.now()
    assign = request.POST['username']
    rows_updated = queryset.update(assign_to=assign,assign_at = timezone.now())
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
    # fields = (
    # 'id', 'project', 'package', 'sequence', 'folder', 'set', 'image_name', 'image_type', 'status', 'assign_to',
    # 'assign_at', 'label_time', 'correction_time', 'loop_on_image', 'file_type', 'created_at')
    # inlines = [ImageInline]
    list_display = ('id','project','package','sequence','folder','set','image_name', 'image_type', 'status', 'assign_to','assign_at','label_time','label_date','correction_time','corrected_date','label_by','corrected_by','loop_on_image','approved_by','approved_date', 'file_type', 'created_at','created_by')
    list_display_links = ('image_name','id')
    search_fields = ('image_name', 'package__package_name', 'status', 'assign_to__username','folder__folder_name',)
    list_filter = (
        ('project', RelatedDropdownFilter),
        ('package', RelatedDropdownFilter),
        ('folder', RelatedDropdownFilter),
        ('set', RelatedDropdownFilter),
        ('assign_to',RelatedDropdownFilter),
        ('image_name',DropdownFilter),
        ('label_date', DateFieldListFilter),
        ('corrected_date', DateFieldListFilter),
        ('created_at', DateFieldListFilter),


    )
    list_per_page = 20

# class ImageAdmin(bulk_admin.BulkModelAdmin):
#     search_fields = ('image_name',)
#     list_display = ('id','project','package','sequence','folder','set','image_name', 'image_type', 'status', 'assign_to','assign_at','label_time','label_date','correction_time','corrected_date','label_by','corrected_by','loop_on_image','approved_by','approved_date', 'file_type', 'created_at')
#     list_filter = ('project','package','folder','set','assign_to',)

class CheckoutResource(resources.ModelResource):

    class Meta:
        model = Checkout
        #exclude = ('label_by',)
        fields = (
        'id','image__image_name', 'image_objects', 'image_status', 'checkin_at', 'checkout_at', 'created_by', 'created_at', 'comment',
    'total_time')
        export_order = (
        'id','image__image_name', 'image_objects', 'image_status', 'checkin_at', 'checkout_at', 'created_by', 'created_at', 'comment',
    'total_time')


class CheckoutAdmin(ImportExportModelAdmin):
    resource_class = CheckoutResource
    list_display = (
    'id','image_id','get_image_name', 'image_objects', 'image_status', 'checkin_at', 'checkout_at', 'created_by', 'created_at', 'comment',
    'total_time')
    search_fields = ('id','created_by__username','image__image_name',)
    list_filter = (
        ('created_by', RelatedDropdownFilter),
    )


class EmployeeResource(resources.ModelResource):

    class Meta:
        model = Employee
        #exclude = ('label_by',)
        fields = (
        'user__username', 'fullname', 'dob', 'department', 'previous_designation', 'designation', 'shift', 'emp_id', 'project',
    'education', 'location', 'experience', 'created_at')
        export_order = (
        'user__username', 'fullname', 'dob', 'department', 'previous_designation', 'designation', 'shift', 'emp_id', 'project',
    'education', 'location', 'experience', 'created_at')

class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('user', 'fullname', 'dob', 'department', 'previous_designation', 'designation', 'shift', 'emp_id', 'project',
    'education', 'location', 'experience', 'created_at')
    #list_display_links = ('image_name','id')
    search_fields = ('fullname',)
    list_filter = ('designation', 'shift','project')
    list_per_page = 30








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

# @admin.register(models.Sequence)
# class SequenceAdmin(bulk_admin.BulkModelAdmin):
#     list_display = ('total_image','sequence_name','sequence_date','project','package','sequence_status','completed_date','uploaded_date','created_at','uploaded_date','created_by','updated_by')
#     search_fields = ('sequence_name', 'sequence_status')

class SequenceResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project',
                           widget=widgets.ForeignKeyWidget(Project, 'project_name'))
    package = fields.Field(column_name='package', attribute='package',
                           widget=widgets.ForeignKeyWidget(Package, 'package_name'))
    folder = fields.Field(column_name='folder', attribute='folder',
                           widget=widgets.ForeignKeyWidget(Folder, 'folder_name'))

    class Meta:
        model = Sequence
        #exclude = ('label_by',)
        fields = ('id','total_image','sequence_name','sequence_date','project','package','folder','sequence_status','completed_date','created_at','uploaded_date','created_by','updated_by')
        export_order = ('id','total_image','sequence_name','sequence_date','project','package','folder','sequence_status','completed_date','created_at','uploaded_date','created_by','updated_by')

@admin.register(models.Sequence)
class SequenceAdmin(ImportExportModelAdmin,):
    resource_class = SequenceResource
    list_display = ('id','total_image','sequence_name','sequence_date','project','package','folder','sequence_status','completed_date','created_at','uploaded_date','created_by','updated_by')
    list_display_links = ('sequence_name','id')
    search_fields = ('sequence_name','sequence_status')
    #list_filter = ('sequence_status', 'project','package','folder')
    list_filter = (
        ('sequence_status', DropdownFilter),
        ('project', RelatedDropdownFilter),
        ('package', RelatedDropdownFilter),
        ('folder', RelatedDropdownFilter),
    )
    list_per_page = 30




@admin.register(models.Set)
class SetAdmin(bulk_admin.BulkModelAdmin):
    list_display = ('total_image','set_name','set_date','project','package','sequence','folder','set_status','completed_date','uploaded_date','created_at','updated_at','created_by','updated_by')
    #search_fields = ('sequence_name', 'sequence_status')

class FolderResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project',
                           widget=widgets.ForeignKeyWidget(Project, 'project_name'))
    package = fields.Field(column_name='package', attribute='package',
                           widget=widgets.ForeignKeyWidget(Package, 'package_name'))

    class Meta:
        model = Folder
        #exclude = ('label_by',)
        fields = ('id',
        'total_image','folder_name','folder_date','project','package','folder_status','completed_date','uploaded_date','created_at','updated_at','created_by','updated_by')
        export_order = (
        'id','total_image','folder_name','folder_date','project','package','folder_status','completed_date','uploaded_date','created_at','updated_at','created_by','updated_by')

@admin.register(models.Folder)
class FolderAdmin(ImportExportModelAdmin):
    resource_class = FolderResource
    list_display = ('id','total_image','folder_name','folder_date','project','package','folder_status','completed_date','uploaded_date','created_at','updated_at','created_by','updated_by')
    list_display_links = ('folder_name','id')
    search_fields = ('folder_name',)
    list_filter = ('folder_status', 'project','package')
    list_per_page = 30

# @admin.register(models.Folder)
# class FolderAdmin(bulk_admin.BulkModelAdmin):
#     list_display = ('total_image','folder_name','folder_date','project','package','folder_status','completed_date','uploaded_date','created_at','updated_at','created_by','updated_by')
    #search_fields = ('sequence_name', 'sequence_status')

# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = (
#     'user', 'fullname', 'dob', 'department', 'previous_designation', 'designation', 'shift', 'emp_id', 'project',
#     'education', 'location', 'experience', 'created_at')




#admin.site.register(Project, ProjectAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Employee, EmployeeAdmin)
#admin.site.register(Package, PackageAdmin)

admin.site.unregister(Set)
admin.site.register(Set,SetAdmin)
admin.site.unregister(Folder)
admin.site.register(Folder,FolderAdmin)
#admin.site.register(Sequence)
admin.site.register(Checkout, CheckoutAdmin)
