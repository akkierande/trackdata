from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView,ListView,CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect,request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

from .models import *
from .models import Image as ImageModel
from .models import Checkout as CheckoutModel
from .forms import *
from .tables import ImageTable,CheckoutTable,CheckoutHistoryTable,PackageTable
from .filters import ImageFilter,CheckoutFilter,PackageFilter
from django_tables2 import RequestConfig, SingleTableView,SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
import datetime


# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating



@login_required(login_url="/accounts/login")
def index(request):
    user_id = request.session.get('_auth_user_id')
    user = User.objects.get(pk=user_id)
    #print(user)
    #user = User.objects.all()
    #employee = Employee.objects.all
    #request.session['username'] = user.username
    #all_images = ImageModel.objects.all()
    #table = ImageindexTable(ImageModel.objects.all())
    # RequestConfig(request,paginate={
    #     'per_page': 5,
    # }).configure(table)



    #RequestConfig(request,'filter':package_filter).configure(table)
    return render(request, 'tracksheet/index.html', {

        'user_id': user_id,
        #'table': table,
        #'filter': ImageFilter,
        #'icks': all_images,
        'user': user,
        #'employee':employee
    })

#
#
# def index(request):
#     return render(request,'tracksheet/index.html',{})




@login_required(login_url="/login")
def userprofile(request):
    if '_auth_user_id' in request.session:
        userId = request.session.get('_auth_user_id')
        user = User.objects.get(pk=userId)
        #print(user)
        #employee = Employee.objects.all()
        #if request.user.is_authenticated:
        #username = request.user.get_username()
        #return user
        #profile = request.user.get_profile()
        return render(request, "tracksheet/profile.html", {})


# class imageDetailView(DetailView):
#     model = Image
#     template_name = 'tracksheet/imgDetail.html'
#
#     def imageView(request, pk=None):
#         # checkout = Checkout.objects.all()
#         qs = get_object_or_404(Image, pk=pk)
#         js = get_object_or_404(CheckoutModel, pk=pk)
#         return render(request, 'tracksheet/imgDetail.html', {'qs': qs})


def imageView(request,pk =None):
    qs = get_object_or_404(Image, pk = pk )
    js = CheckoutModel.objects.filter(image_id__pk=qs.id)
    table = CheckoutHistoryTable(js)
    RequestConfig(request).configure(table)
    return render(request, 'tracksheet/imgDetail.html',{'table': table,'qs': qs,'icks':js})

# def CheckoutView(request, pk):
#     check = CheckoutModel.objects.filter(image_id__id = pk).all()
#     if request.method == 'POST':
#         form = CheckoutForm(request.POST,instance=check)
#         template_name = 'tracksheet/checkout.html'
#         context = {
#             "form": form,
#             # "title": qs.title,
#
#         }
#         return render(request, template_name, context)
    # model = Checkout
    # qs = get_object_or_404()
    # Checkout.image_id = Image.id
    # qs = get_object_or_404(Checkout, =pk)
    #qs = Checkout.objects.filter(checkout__image_id=pk)
    #form = CheckoutForm(request.POST or None,instance=check)

    # form_class = CheckoutForm


# class Checkout_History_Table(FilterView, ExportMixin, SingleTableView):
#     table_class = CheckoutHistoryTable
#     model = Checkout
#     paginate_by = 10
#     template_name = 'tracksheet/checkout_history.html'
#     filterset_class = CheckoutFilter



class Image_Table(FilterView, ExportMixin, SingleTableView):
    table_class = ImageTable
    model = Image
    paginate_by = 10
    #RequestConfig(request, paginate={'per_page': 25}).configure(ImageTable)
    template_name = 'tracksheet/image_table.html'
    filterset_class = ImageFilter

class Package_Table(FilterView, ExportMixin, SingleTableView):
    table_class = PackageTable
    model = Package
    paginate_by = 5
    #RequestConfig(request, paginate={'per_page': 25}).configure(ImageTable)
    template_name = 'tracksheet/index.html'
    #filterset_class = PackageFilter





class Checkout_Table(FilterView, ExportMixin, SingleTableView):
    table_class = CheckoutTable
    model = Checkout
    paginate_by = 10
    template_name = 'tracksheet/checkout_table.html'
    filterset_class = CheckoutFilter


def checkoutimage(request,pk=None):
    qs = get_object_or_404(Image,pk = pk)
    icks = CheckoutModel.objects.filter(image_id__pk = qs.id)
    return render(request,'tracksheet/imagecheckout.html',{'icks':icks})





def editCheckout(request,pk=None):
    instance = get_object_or_404(CheckoutModel,pk = pk)
    #print(instance.checkout_at)
    form = CheckoutForm(request.POST or None, instance=instance)
    #print(instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    context = {
        # "title": qs.title,
        "instance": instance,
        "form": form,
    }
    return render(request, 'tracksheet/checkout.html', context)

def addCheckout(request,pk=None):
    instance = get_object_or_404(ImageModel, pk=pk)
    #qs = get_object_or_404(Image, pk=pk)
    #print (instance)
    form = CheckoutForm(request.POST or None,initial={'image_id': instance})
    #print (form)

    checkout_of = CheckoutModel.objects.filter(image_id__pk=instance.id)
    table = CheckoutHistoryTable(checkout_of)
    RequestConfig(request).configure(table)

    #form = CheckoutForm(request.POST or None)
    #instance = get_object_or_404(CheckoutModel,pk = pk)
    #form = JournalForm(initial={'tank': 123})
    if form.is_valid():
        print (instance)
        instance = form.save(commit=False)
        instance.save()
        HttpResponseRedirect("/tracksheet/checkout")

    context = {
        # "title": qs.title,
        "checkout_of":checkout_of,
        "instance": instance,
        "form": form,
        'table':table,
        #"template_name": 'tracksheet/addcheckout.html',
    }
    return render(request, 'tracksheet/addcheckout.html', context)






































#
# class CheckoutCreateView(CreateView,SingleTableMixin):
#     model = CheckoutModel
#     form_class = CheckoutForm
#     context = {form_class': CheckoutForm}
#     template_name ='tracksheet/addcheckout.html'
#     success_url = 'success'
#
#     def get_context_data(self, **kwargs):
#         instance = CheckoutModel.objects.get(**kwargs)
#         chk = CheckoutModel.objects.filter(image_id__pk=instance.id)
#
#     def render_to_response(self, context, **response_kwargs):
#         return super(CheckoutCreateView, self).render_to_response(context, **response_kwargs)


   # @method_decorator(login_required)
   # def dispatch(self,request, *args, **kwargs):
   #     return super(ImageView, self).dispatch(request,*args, **kwargs)


        #
# class Project_View(FilterView, ExportMixin, SingleTableView):
#     table_class = ProjectTable
#     model = Project
#     template_name = 'tracksheet/table.html'
#     filterset_class = ProjectFilter



# class CheckoutView(,(getattr(pk))):
#    model = CheckoutModel
#    pk = CheckoutModel.pk
#    #context_object_name = 'user_checkout_list'
#    user_checkout_list = CheckoutModel.objects.filter(image_id__id = pk).all()
#    #queryset = check.filter()
#    form_class = CheckoutForm
#    template_name = 'checkout.html'
#
#    def form_valid(self, form):
#       self.object = form.save(commit=False)
#       # Any manual settings go here
#       self.object.save()
#       return HttpResponseRedirect(self.object.get_absolute_url())
#
#    @method_decorator(login_required)
#    def dispatch(self, request, *args, **kwargs):
#      return super(CheckoutView, self).dispatch(request, *args, **kwargs)









#
# class CheckoutImageListView(ListView):
#     model = CheckoutModel
#     template_name = 'tracksheet/imagecheckout.html'
#
#     def get_queryset(self):
#         qs = get_object_or_404(CheckoutModel,pk = self.kwargs['pk'])
#         icks = Image.objects.filter(image_name = qs)
#         #print(icks['image_type'])
#         #return icks
#         #self.checkout = get_object_or_404(CheckoutModel,pk = self.kwargs['pk'])
#         #print(qs)
#         #print(imagecheckouts)
#         #return super(CheckoutImageListView, self).dispatch(request,'tracksheet/imagecheckout.html',{'qs':imagecheckouts})
#         #return HttpResponseRedirect(imagecheckouts.get_absolute_url())
#         #return render(request,'tracksheet/imagecheckout.html',{'qs':imagecheckouts})
#         #return render(request, 'polls/detail.html', {'question': question})



   # def view(request):
   #     return render_to_response('mainview.html', {
   #         'entryquery': Checkout.objects.all(),
   #     }
   #                               )



# tutorial/views.py

#
# class Package_View(FilterView, ExportMixin, SingleTableView):
#     table_class = PackageTable
#     model = Package
#     template_name = 'tracksheet/table.html'
#     filterset_class = PackageFilter

# def image(request, user_id=None):
#     profile = request.user.get_profile()
#
#     if user_id is None:
#         contact = Contact(company=profile.company)
#         template_title = _(u'Add Contact')
#     else:
#         contact = get_object_or_404(profile.company.contact_set.all(), pk=contact_id)
#         template_title = _(u'Edit Contact')
#
#     if request.POST:
#         if request.POST.get('cancel', None):
#             return HttpResponseRedirect('/')
#         form = ImageForm(profile.company, request.POST, instance=contact)
#         if form.is_valid():
#             image = form.save()
#             return HttpResponseRedirect('/')
#     else:
#         form = ContactsForm(instance=contact, company=profile.company)
#         variables = RequestContext(request, {'form':form, 'template_title': template_title})
#         return render_to_response("contact.html", variables)
