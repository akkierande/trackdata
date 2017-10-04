import django_tables2 as tables
from .models import Image
from django_tables2.utils import A

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
#         #template_name = 'tracksheet/image_table.html'

class ImageTable(tables.Table):
    Image.image_name = tables.LinkColumn('image_name', args=[A('pk')])
    class Meta:
        model = Image
        row_attrs = {'image_id': lambda record: record.pk}
        name = tables.LinkColumn('image_edit', text=lambda image: image.image_name, args=[A('pk')])
        edit_entries = tables.TemplateColumn('<a href="/tracksheet/image/{{image.image_name}}">Edit</a>')
        exclude = ['created_at', 'updated_at','created_by','updated_by']
        empty_text = "There are no Images matching the search criteria..."
        #template_name = 'tracksheet/image_table.html'

