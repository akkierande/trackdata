from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import *
from .forms import *

from .tables import ImageTable,CheckoutTable
from .filters import PackageFilter, ImageFilter,CheckoutFilter, ProjectFilter
from django_tables2 import RequestConfig, SingleTableView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
import datetime



total_count = User.objects.count()
# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="/accounts/login")
def index(request):
    user = request.session.get('user')
    #all_packages = Package.objects.all()
    all_images = Image.objects.all()
    #all_projects = Project.objects.all()
    table = ImageTable(Image.objects.all())
    #total_count = User.objects.count()
    # RequestConfig(request,'filter':package_filter).configure(table)
    return render(request, 'tracksheet/index.html', {
        'table': table,
        'all_images': all_images,
        'total_count': total_count,
    })


@login_required(login_url="/login")
def detail(request, project_id):
    return HttpResponse("<h2>Details for Project id:" + str(project_id) + "</h2>")


# tutorial/views.py


@login_required(login_url="/login")
def userprofile(request,total_count):
    if User is not None and User.is_active:
        # Correct password, and the user is marked "active"
        user = User.objects.all()
        return render(request, "tracksheet/profile.html", {'user': user,'total_count': total_count,})
    else:
        # Show an error page
        return "Error"

#
class CheckoutCreateView(CreateView):
   model = Checkout
   fields = ['checkout_at','image_objects','comment']
   #form_class = CheckoutForm
   template_name = 'tracksheet/checkout.html'

   def form_valid(self, form):
      self.object = form.save(commit=False)
      # any manual settings go here
      self.object.save()
      return HttpResponseRedirect(self.object.get_absolute_url())

   @method_decorator(login_required)
   def dispatch(self, request, *args, **kwargs):
      return super(CheckoutCreateView, self).dispatch(request, *args, **kwargs)
#
#
# class CheckoutUpdateView(UpdateView):
#    model = Checkout
#    form_class = CheckoutForm
#    template_name = 'form.html'
#
#    def form_valid(self, form):
#       self.object = form.save(commit=False)
#       # Any manual settings go here
#       self.object.save()
#       return HttpResponseRedirect(self.object.get_absolute_url())
#
#    @method_decorator(login_required)
#    def dispatch(self, request, *args, **kwargs):
#      return super(CheckoutUpdateView, self).dispatch(request, *args, **kwargs)

def package_delete(request,pk):
    return HttpResponse('This is a delete page!')


def image_edit(request, pk):
    return HttpResponse('This is an edit page!')

#
# class Package_View(FilterView, ExportMixin, SingleTableView):
#     table_class = PackageTable
#     model = Package
#     template_name = 'tracksheet/table.html'
#     filterset_class = PackageFilter


class Image_View(FilterView, ExportMixin, SingleTableView):
    table_class = ImageTable
    model = Image
    template_name = 'tracksheet/table.html'
    filterset_class = ImageFilter

class Checkout(FilterView, ExportMixin, SingleTableView):
    table_class = CheckoutTable
    model = Checkout
    template_name = 'tracksheet/table1.html'
    filterset_class = CheckoutFilter

        #
# class Project_View(FilterView, ExportMixin, SingleTableView):
#     table_class = ProjectTable
#     model = Project
#     template_name = 'tracksheet/table.html'
#     filterset_class = ProjectFilter




# def renew_book_librarian(request, pk):
#     book_inst=get_object_or_404(, pk = pk)
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#
#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)
#
#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_inst.due_back = form.cleaned_data['renewal_date']
#             book_inst.save()
#
#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('all-borrowed') )
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
#
#     return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})