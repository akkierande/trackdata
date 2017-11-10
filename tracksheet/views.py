from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView,ListView,CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect,request
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import Group

from .models import *
from .models import Image as ImageModel
from .models import Checkout as CheckoutModel
from .forms import *
from .tables import ImageTable,CheckoutTable,CheckoutHistoryTable,PackageTable,ProjectTable
from .filters import ImageFilter,CheckoutFilter,PackageFilter,ProjectFilter
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
    return render(request, 'tracksheet/index.html', {

        'user_id': user_id,
        #'table': table,
        #'filter': ImageFilter,
        #'icks': all_images,
        'user': user,
        #'employee':employee
    })

@login_required(login_url="/login")
def userprofile(request):
    if '_auth_user_id' in request.session:
        userId = request.session.get('_auth_user_id')
        user = User.objects.get(pk=userId)
        return render(request, "tracksheet/profile.html", {})

@login_required(login_url="/login")
def imageView(request,pk =None):
    qs = get_object_or_404(Image, pk = pk )
    js = CheckoutModel.objects.filter(image_name__pk=qs.id)
    table = CheckoutHistoryTable(js)
    RequestConfig(request,paginate={'per_page': 10}).configure(table)
    return render(request, 'tracksheet/imgDetail.html',{'table': table,'qs': qs,'icks':js})

class Image_Table(FilterView, ExportMixin, SingleTableView):
    table_class = ImageTable
    model = Image
    paginate_by = 10
    #RequestConfig(request, paginate={'per_page': 25}).configure(ImageTable)
    template_name = 'tracksheet/image_table.html'
    filterset_class = ImageFilter

#request.user.groups.filter(name__in=['onetime','monthtime']).exists()



#@user_passes_test(lambda u: u.groups.filter(name='admin').count() == 0, login_url='/tracksheet/restricted')

class Package_Table(FilterView, ExportMixin, SingleTableView,PermissionRequiredMixin):
    table_class = PackageTable
    model = Package
    paginate_by = 10
    #RequestConfig(request, paginate={'per_page': 25}).configure(ImageTable)
    template_name = 'tracksheet/package_table.html'
    filterset_class = PackageFilter


class Project_Table(FilterView, ExportMixin, SingleTableView):
    table_class = ProjectTable
    model = Project
    paginate_by = 10
    #RequestConfig(request, paginate={'per_page': 25}).configure(ImageTable)
    template_name = 'tracksheet/project_table.html'
    filterset_class = ProjectFilter

class Checkout_Table(FilterView, ExportMixin, SingleTableView):
    table_class = CheckoutTable
    model = Checkout
    paginate_by = 10
    template_name = 'tracksheet/checkout_table.html'
    filterset_class = CheckoutFilter

def checkoutimage(request,pk=None):
    qs = get_object_or_404(Image,pk = pk)
    icks = CheckoutModel.objects.filter(image_name = qs.image_name)
    print(icks)
    return render(request,'tracksheet/imagecheckout.html',{'icks':icks})

#<QuerySet [<Group: Labeller>, <Group: Quality Check>, <Group: Quality2>, <Group: Team Lead>, <Group: Team Head>, <Group: Data analyst>, <Group: Employee>, <Group: Super Admin>, <Group: admin>]>
def editCheckout(request,pk=None):
    instance = get_object_or_404(CheckoutModel,pk = pk)
    id = Checkout.get_image_id(instance)
    print (instance.image_name)
    #print(instance.checkout_at)
    form = CheckoutForm(request.POST or None,initial={'image_name': instance.image_name},instance=instance)
    #print(instance)
    if form.is_valid():
        l_time = 0
        instance = form.save(commit=False)
        checkin = form.cleaned_data['checkin_at']
        checkout = form.cleaned_data['checkout_at']
        image_status = form.cleaned_data['image_status']
        #print (checkin)
        #print (checkout)
        if checkin is not None:
            if checkin >= checkout:
                instance.total_time = checkin-checkout
                l_time = str(instance.total_time)
            else:
                messages.error(request,'enter Valid date-time')
                return redirect('edit_checkout', pk=pk)
        image = Image.objects.get(pk=id)
        print(image_status)
        print(image)
        if image_status=='Labelled':
            image.status = 'Labelled'
            image.label_time = sum(l_time)
            image.save()


        instance.created_by = request.user
        instance.save()
        messages.success(request, 'Checkout successful')
        return redirect('edit_checkout', pk=pk)

    context = {
        # "title": qs.title,
        'id':id,
        "instance": instance,
        "form": form,
    }
    return render(request, 'tracksheet/checkout.html', context)


def get_check_date(request,pk):
    qs = get_object_or_404(CheckoutModel,pk=pk)
    return qs.checkin_at

def addCheckout(request,pk=None):
    qs = CheckoutModel.objects.all()
    instance = get_object_or_404(ImageModel, pk=pk)
    checkout_instance = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    form = CheckoutForm(request.POST or None,initial={'image_name': instance,'checkout_at':checkout_instance})
    checkout_of = CheckoutModel.objects.filter(image_name__pk=instance.id)
    table = CheckoutHistoryTable(checkout_of)
    RequestConfig(request,paginate={'per_page': 10}).configure(table)

    if form.is_valid():
        print(dir())
        print (instance)
        print (form.cleaned_data['image_name'])
        send_data = instance
        get_data = form.cleaned_data['image_name']
        #print (instance)
        instance = form.save(commit=False)
        checkout = form.cleaned_data['checkout_at']
        checkin = form.cleaned_data['checkin_at']
        instance.created_by = request.user
        #instance.total_time = checkin + checkout
        print (instance.total_time)
        if send_data == get_data:
            instance.save()
        else:
            messages.error(request, 'You cannot Change Others Image')
            return redirect('add_checkout', pk=pk)
        messages.success(request, 'Checkout successful')
        return redirect('add_checkout', pk=pk)
        #return redirect('/tracksheet/checkout/', {'messages': messages})
        #return redirect('/tracksheet/checkout/')
    context = {
        # "title": qs.title,
        "checkout_of":checkout_of,
        "instance": instance,
        "form": form,
        'table':table,
        #"template_name": 'tracksheet/addcheckout.html',
    }
    return render(request, 'tracksheet/addcheckout.html', context)



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
