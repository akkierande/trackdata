from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView,ListView,CreateView,View
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect,request
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import Group
from avatar.models import Avatar
from django.db.models import Sum
from django.db.models import Q
from django.utils.timesince import timesince


from .models import *
from .models import Image as ImageModel
from .models import Checkout as CheckoutModel
from .forms import *
from .tables import ImageTable,CheckoutTable,CheckoutHistoryTable,PackageTable,ProjectTable,MyImageTable
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
    Projects = Project.objects.all()
    return render(request, 'tracksheet/index.html', {
        'projects':Projects,
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
        form = EmployeeDetailForm()
        user = User.objects.get(pk=userId)
        #print(Avatar.user)
        return render(request, "tracksheet/profile.html", {'form':form})

@login_required(login_url="/login")
def imageView(request,pk = None):
    qs = get_object_or_404(Image, pk = pk )
    js = CheckoutModel.objects.filter(image_id=qs.id)
    table = CheckoutHistoryTable(js)
    RequestConfig(request,paginate={'per_page': 10}).configure(table)
    return render(request, 'tracksheet/imgDetail.html',{'table': table,'qs': qs,'icks':js})

class Image_Table(FilterView, ExportMixin, SingleTableView):
    table_class = ImageTable
    model = Image
    paginate_by = 10
    template_name = 'tracksheet/image_table.html'
    filterset_class = ImageFilter
    #get_current_path(request)


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


def get_current_path(request):
    current_url = request.get_full_path()
    return current_url
    #print (current_url)
    # return {
    #    'current_path': request.get_full_path()
    #  }



def checkoutimage(request,pk=None):
    qs = get_object_or_404(Image,pk = pk)
    icks = CheckoutModel.objects.filter(image_name = qs.image_name)
    print(icks)
    return render(request,'tracksheet/imagecheckout.html',{'icks':icks})


def get_check_date(request,pk):
    qs = get_object_or_404(CheckoutModel,pk=pk)
    return qs.checkin_at

def get_label_time(i_status,pk=None):
    instance = get_object_or_404(ImageModel, pk=pk)
    if i_status=='InProcess' or i_status=='Labelled' or i_status=='Corrected':
        total_label_time = (CheckoutModel.objects.filter(Q(image_id__pk=instance.id),Q(image_status = "Labelled") | Q(image_status = "InProcess") | Q(image_status = "Corrected")).aggregate(total=Sum('total_time'))['total'])
        print (total_label_time)
        instance.label_time = total_label_time
    elif i_status == 'ChangeNeeded' or i_status == 'InQuality' or i_status == 'Approved':
        total_correction_time = (CheckoutModel.objects.filter(Q(image_id__pk=instance.id),Q(image_status = "ChangeNeeded") | Q(image_status = "InQuality") | Q(image_status = "Approved")).aggregate(total=Sum('total_time'))['total'])
        print(total_correction_time)
        instance.correction_time = total_correction_time
    chkinstance = CheckoutModel.objects.filter(image_id__pk=instance.id, image_status="ChangeNeeded").count()
    instance.loop_on_image = chkinstance
    instance.status = i_status
    instance.save()


#<QuerySet [<Group: Labeller>, <Group: Quality Check>, <Group: Quality2>, <Group: Team Lead>, <Group: Team Head>, <Group: Data analyst>, <Group: Employee>, <Group: Super Admin>, <Group: admin>]>
def editCheckout(request,pk=None):
    chkout = get_object_or_404(CheckoutModel,pk = pk)
    image_name = Checkout.get_image_name(chkout)
    form = CheckoutForm(request.POST or None,initial={'image_id': chkout.image},instance=chkout)
    if form.is_valid():
        instance = form.save(commit=False)
        checkin = form.cleaned_data['checkin_at']
        checkout = form.cleaned_data['checkout_at']
        i_status = form.cleaned_data['image_status']
        if checkin is not None:
            if checkin >= checkout:
                total_time = checkin-checkout
                days, seconds = total_time.days, total_time.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                instance.total_time = datetime.timedelta(days=days,hours=hours,minutes=minutes)
            else:
                messages.error(request,'enter Valid date-time')
                return redirect('edit_checkout', pk=pk)

        instance.created_by = request.user
        instance.save()
        get_label_time(i_status, pk=chkout.image.pk)
        messages.success(request, 'Checkout successful')
        return redirect('edit_checkout', pk=pk)

    context = {

        'id':chkout.image.pk,
        "instance": image_name,
        "form": form,
    }
    return render(request, 'tracksheet/editcheckout.html', context)

def addCheckout(request,pk=None):
    image = get_object_or_404(ImageModel, pk=pk)
    print (image.image_name)
    checkout_instance = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    form = CheckoutForm(request.POST or None,initial={'image':image,'checkout_at':checkout_instance})
    checkout_of = CheckoutModel.objects.filter(image = image.id)
    table = CheckoutHistoryTable(checkout_of)
    RequestConfig(request,paginate={'per_page': 10}).configure(table)
    if form.is_valid():
        instance = form.save(commit=False)
        checkout = form.cleaned_data['checkout_at']
        checkin = form.cleaned_data['checkin_at']
        i_status = form.cleaned_data['image_status']
        instance.created_by = request.user
        instance.image_id = image.id
        #send_data = str(image.id)
        # print (send_data)
        #get_data = form.cleaned_data['image_id']
        # print (get_data)
        # if send_data == str(get_data):
        #     instance.save()
        # else:
        #     messages.error(request, 'You cannot Change Others Image')
        #     return redirect('add_checkout', pk=pk)
        if checkin is not None:
            if checkin >= checkout:
                total_time = checkin-checkout
                days, seconds = total_time.days, total_time.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                instance.total_time = datetime.timedelta(days=days,hours=hours,minutes=minutes)
            else:
                messages.error(request,'enter Valid date-time')
                return redirect('add_checkout',pk=pk)
                #return render(request,'tracksheet/add_checkout.html', {'pk': pk, 'form': form})

        get_label_time(i_status,pk=pk)
        instance.save()
        messages.success(request, 'Checkout successful')
        return redirect('add_checkout', pk=pk)
    context = {
        "checkout_of":checkout_of,
        "instance":image.image_name,
        "form": form,
        'table':table,
    }
    return render(request, 'tracksheet/addcheckout.html', context)

from django.http import JsonResponse
from tracksheet.templatetags import tags

class DisplayView(View):
    def get(self, request, *args, **kwargs):
        project = Project.objects.all()
        return render(request, 'tracksheet/image-graph.html',{'all_projects':project})


@login_required(login_url="/login")
def MyimageView(request):
    #qs = get_object_or_404(Image)
    js = ImageModel.objects.filter(assign_to=request.user)
    f = ImageFilter(request.GET, queryset=js)
    table = MyImageTable(js)
    RequestConfig(request,paginate={'per_page': 10}).configure(table)
    return render(request, 'tracksheet/assign_table.html',{'table': table,'filter': f})


def articleView(request):
    return render(request, 'tracksheet/article.html')




class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tracksheet/charts.html')

def get_data(request , pk):
    print ("primary key" + str(pk))
    if not (pk == 0):
        image_piechart = tags.image_piechart(request,pk)
        #total_labels = 200
        labels = ["Unlabelled", "Labelled", "In-Process", "Corrected", "Change-Needed", "In Quality","Approved","Uploaded"]
        default_items = image_piechart
        data = {
            "labels": labels,
            "default": default_items,
        }
        return JsonResponse(data) # http response
    else:
        print ("No Data Found")

# def get_project(request,project_name,*args,**kwargs):
#     project_list = get_object_or_404(Project, project_name=project_name)
#     if request.method == 'POST':
#         print(request)
#         print (project_name )
#         form = ProjectListForm(request.POST,project_list)
#         if form.is_valid():
#             return redirect(request.path)
#     else:
#         form = ProjectListForm()
#         context = {
#             "form": form,
#         }
#         return render(request, 'tracksheet/images/charts.html', context)


from forms import EmployeeDetailForm
def employee_details(request):
    #print ("Hi")
    if request.method == 'POST':
        form = EmployeeDetailForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = EmployeeDetailForm()
    return render(request, 'tracksheet/profile.html', {'form': form})