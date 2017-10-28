import django_tables2 as tables
from .models import Image,Checkout
from django_tables2.utils import A
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

class ImageTable(tables.Table):

    view = tables.TemplateColumn('<button type="button" class="btn btn-info btn-xs"><a href="/tracksheet/images/{{record.id}}"> Details </a></button>')
    #Editcheckout = tables.TemplateColumn('<button type="button" class="btn btn-warning btn-xs"><a href="/tracksheet/checkout/edit/{{record.id}}">Edit</a></button>')
    checkout = tables.TemplateColumn('<button type="button" class="btn btn-warning btn-xs"><a href="/tracksheet/checkout/add/{{record.id}}">Checkout</a></button>')

    image_name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')],orderable=True,verbose_name='Image Name')
    class Meta:
        model = Image
        exclude = ['updated_at','updated_by','file_type','status','image_type']
        empty_text = "There are no Images matching the search criteria..."
        sequence = ('id','project','package','image_name','created_at','created_by','view',)
        id = id


class CheckoutTable(tables.Table):

    #Image.image_name = tables.LinkColumn('image', args=[A('pk')])
    #name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')])
    image_id = tables.LinkColumn('image', args=[A('pk')],text=lambda image: image.image_id, orderable=True, empty_values=())
    checkout = tables.TemplateColumn('<button type="button" class="btn btn-warning btn-xs"><a href="/tracksheet/checkout/add/{{record.id}}">Checkout</a></button>')

    class Meta:
        model = Checkout
        sequence = ('id','image_id','image_status','image_objects','checkout_at','checkin_at','comment')
        #exclude = ('image_id')
        #row_attrs = {'image_id': lambda record: record.pk}
        #edit_entries = tables.TemplateColumn('<a href="/tracksheet/image/{{image.image_name}}">Edit</a>')
        empty_text = "There are no Images matching the search criteria..."
        #sequence = ('Image_Name','image_type')
        #template_name = 'tracksheet/image_table.html'


class CheckoutHistoryTable(tables.Table):

    #Image.image_name = tables.LinkColumn('image', args=[A('pk')])
    #name = tables.LinkColumn('image', text=lambda image: image.image_name, args=[A('pk')])
    #image_id = tables.LinkColumn('image', args=[A('pk')],text=lambda image: image.image_id, orderable=True, empty_values=())
    Edit = tables.TemplateColumn('<button type="button" class="btn btn-warning btn-xs"><a href="/tracksheet/checkout/edit/{{record.id}}">Edit</a></button>')
    image_status = tables.TemplateColumn('<span class="label label-success">{{record.image_status}}</span>',verbose_name="Status")
    class Meta:
        model = Checkout
        sequence = ('id','image_id','created_by','checkin_at','checkout_at','image_status','image_objects','comment')
        #exclude = ('image_id')
        #row_attrs = {'image_id': lambda record: record.pk}
        #edit_entries = tables.TemplateColumn('<a href="/tracksheet/image/{{image.image_name}}">Edit</a>')
        empty_text = "There are no Checkout matching the search criteria..."
        #sequence = ('Image_Name','image_type')
        #template_name = 'tracksheet/image_table.html'
