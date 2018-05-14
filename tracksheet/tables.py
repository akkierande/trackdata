import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable
from .models import Image,Checkout,Package,Project
from django_tables2.utils import A
import itertools
from django.contrib.auth import models
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.http import request



# class PackageTable(tables.Table):
#     name = tables.LinkColumn('package_edit',text=lambda package: package.package_name, args=[A('pk')])
#     list_display_links = ('id', 'title')
#
#     #sel = tables.CheckBoxColumn(accessor="pk", orderable=False)
#     # edit_entries = tables.TemplateColumn('<a href="/tracksheet/package/{{package.package_name}}">Edit</a>')
#     # #editable = tables.LinkColumn('edit_form', verbose_name='edit')
#     # edit_link = tables.LinkColumn('package_edit', args=[A('pk')],attrs= { 'format_html': '<a><b>EDIT</b></a>','href':'#{{client.pk}}'}, verbose_name='Edit' , text='Edit')
#     # delete_link = tables.LinkColumn('package_delete', args=[A('pk')],attrs= { 'format_html': '<a><b>DELETE</b></a>'}, verbose_name='delete',text='Delete' )
#     #edit_link = tables.LinkColumn('bug_edit', args=[A('pk')],verbose_name='Edit', accessor='pk', attrs={'class': 'edit_link'})
#     class Meta:
#         model = Package
#         empty_text = "There are no Packages matching the search criteria..."
#
#         #
#
#         #template_name = 'tracksheet/image_table.html'  /tracksheet/images/{{record.id}}  <a data-toggle="modal" href="#imageModal">Checkout</a>

class ImageTable(ColumnShiftTable):

    view = tables.TemplateColumn('<a href="/tracksheet/images/{{record.id}}"><button type="button" class="btn btn-info btn-xs"> Details </button></a>')
    #Editcheckout = tables.TemplateColumn('<button type="button" class="btn btn-warning btn-xs"><a href="/tracksheet/checkout/edit/{{record.id}}">Edit</a></button>')
    checkout = tables.TemplateColumn('<a href="/tracksheet/checkout/add/{{record.id}}"><button type="button" class="btn btn-warning btn-xs">Checkout</button></a>')

    image_name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')],orderable=True,verbose_name='Image Name')
    class Meta:
        model = Image
        #attrs = {'class': 'column-shifter-container table-responsive'}
        exclude = ['updated_at','updated_by','created_at','created_by','file_type','image_type','approved_date','id','assign_at','loop_on_image']
        empty_text = "There are no Images matching the search criteria..."
        sequence = ('id','project','package','folder','sequence','set','image_name','status','label_time','correction_time')
        id = id
        order_by = 'image_name'


class CheckoutTable(tables.Table):
    #image_name = tables.Column(accessor='image_id',)

    #Image.image_name = tables.LinkColumn('image', args=[A('pk')])
    #name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')])
    #image_name = tables.LinkColumn('image', args=[A('image_id')], text= lambda Image: Image.image_id, orderable=True, empty_values=())
    image_name = tables.LinkColumn('image', args=[A('image.id')],text= lambda image: image.image.image_name,orderable=True,empty_values=())
    #print (image.image_name)
    #imagid = Image.pk

    edit = tables.TemplateColumn('<a href="/tracksheet/checkout/edit/{{record.id}}"><button type="button" class="btn btn-warning btn-xs">Edit</button></a>')

    class Meta:
        model = Checkout
        sequence = ('id','image_name','image_status','image_objects','checkout_at','checkin_at','comment')
        #qs = Image.objects.filter(CheckoutTable=Image.pk)
        exclude = ('image','scene_type',
            'weather',
            'day_lights',
            'no_of_scooters',
            'scooter_group',
            'no_of_motorbike',
            'motorbike_group',
            'no_of_bicycle',
            'no_of_mistakes',
            'bicycle_group',
            'other_tag_issues',
            'occlusion_truncation_issues',
            'total_unique_bicycle',
            'total_unique_scooter',
            'total_unique_motorbike',
            'total_unique_objects',)
        #row_attrs = {'image_name': lambda record:getattr(Image,'image_name')}
        #edit_entries = tables.TemplateColumn('<a href="/tracksheet/image/{{image.image_name}}">Edit</a>')
        empty_text = "There are no Images matching the search criteria..."
        #sequence = ('Image_Name','image_type')
        #template_name = 'tracksheet/image_table.html'

    # def __init__(self, *args, **kwargs):
    #     if kwargs.pop("popup", False):
    #         for column in self.base_columns.values():
    #             if isinstance(column, tables.LinkColumn):
    #                 column.args.insert(0, "popup")
    #     super(Table, self).__init__(*args, **kwargs)


class CheckoutHistoryTable(tables.Table):
    #image_name = tables.Column(accessor='Image.image_name')

    #Image.image_name = tables.LinkColumn('image', args=[A('pk')])
    #name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')])
    #id = tables.TemplateColumn('id',text = lambda image:image.image.pk,order_by='-id')
    image_name = tables.LinkColumn('image', args=[A('image.id')], text=lambda image: image.image.image_name,
                                   orderable=True, empty_values=())
    #image_id = tables.LinkColumn('image', args=[A('image_id')], text=lambda image: image.image_name, orderable=True,empty_values=())
    Edit = tables.TemplateColumn('<a href="/tracksheet/checkout/edit/{{ record.id }}"><button type="button" class="btn btn-warning btn-xs">Check-IN</button></a>')
    #Delete = tables.TemplateColumn('<a href="/tracksheet/checkout/delete/{{record.id}}"><button type="button" class="btn btn-danger btn-xs">Delete</button></a>')
    image_status = tables.TemplateColumn('<span class="label label-success">{{record.image_status}}</span>',verbose_name="Status")

    class Meta:
        model = Checkout
        sequence = ('id','image_name','created_by','checkout_at','checkin_at','image_status','image_objects','comment')
        exclude = ('image','scene_type','weather','day_lights','no_of_scooters','scooter_group','no_of_motorbike','motorbike_group','no_of_bicycle','no_of_mistakes','bicycle_group','other_tag_issues',
                   'occlusion_truncation_issues','total_unique_bicycle','total_unique_scooter','total_unique_motorbike','total_unique_objects',)
        #row_attrs = {'image_name': lambda record:}
        #edit_entries = tables.TemplateColumn('<a href="/tracksheet/image/{{image.image_name}}">Edit</a>')
        empty_text = "There are no Checkout matching the search criteria..."
        #sequence = ('Image_Name','image_type')
        #template_name = 'tracksheet/image_table.html'
        order_by = '-created_at'

class PackageTable(ColumnShiftTable):
    #image_name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')],orderable=True,verbose_name='Image Name')
    class Meta:
        model = Package
        exclude = ['completed_date','updated_at','updated_by']
        empty_text = "There are no Packages matching the search criteria..."
        sequence = ('id','package_name','total_image','package_date','project','package_status','uploaded_date','created_at','created_by')
        #id = id


class ProjectTable(ColumnShiftTable):


    #total_packages = tables.LinkColumn('package', text=lambda package: package.total_packages, args=[A('get_total_packages')],orderable=True,verbose_name='Image Name')
    class Meta:
        model = Project
        exclude = ['completed_date','uploaded_date','updated_at','updated_by']
        empty_text = "There are no Projects matching the search criteria..."
        sequence = ('id','project_name','customer','project_type','start_date','end_date','resources','total_packages','current_uploaded','project_status')
        #id = id

class AssignTable(ColumnShiftTable):

    view = tables.TemplateColumn(
        '<a href="/tracksheet/images/{{record.id}}"><button type="button" class="btn btn-info btn-xs"> Details </button></a>')
    # Editcheckout = tables.TemplateColumn('<button type="button" class="btn btn-warning btn-xs"><a href="/tracksheet/checkout/edit/{{record.id}}">Edit</a></button>')
    checkout = tables.TemplateColumn(
        '<a href="/tracksheet/checkout/add/{{record.id}}"><button type="button" class="btn btn-warning btn-xs">Checkout</button></a>')

    image_name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')], orderable=True,
                                   verbose_name='Image Name')

    class Meta:
        model = Image
        exclude = ['updated_at', 'updated_by','created_at','created_by', 'file_type', 'image_type']
        empty_text = "There are no Images matching the search criteria..."
        sequence = ('id', 'project', 'package', 'folder', 'sequence', 'set','image_name', 'status', 'label_time', 'correction_time', 'loop_on_image')
        order_by = '-assign_at'
        #id = id