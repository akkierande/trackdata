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
from .mixins import GroupRequiredMixin
from django.template.loader import render_to_string
from .models import *
from .models import Image as ImageModel
from .models import Checkout as CheckoutModel
from .forms import *
from .tables import ImageTable,CheckoutTable,CheckoutHistoryTable,PackageTable,ProjectTable,AssignTable
from .filters import ImageFilter,CheckoutFilter,PackageFilter,ProjectFilter,AssignFilter
from django_tables2 import RequestConfig, SingleTableView,SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
import datetime
from .admin import ImageResource
# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating


# from django.core.mail import EmailMessage
# title = "Trackpro Password Reset"
# email = EmailMessage('title', 'body', to=[email])
# email.send()



@login_required(login_url="/accounts/login")
#from pinax.messages.models import Message

def index(request):
   # Message.new_message(from_user=request.user, to_users=[user], subject=subject, content=content)
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
    permission_required = 'package.view_package'
    table_class = PackageTable
    model = Package
    paginate_by = 10
    #group_required = ["admin","manager","Labeller"]
    template_name = 'tracksheet/package_table.html'
    filterset_class = PackageFilter

class Assign_Table(FilterView, ExportMixin, SingleTableView):
    table_class = AssignTable
    model = Image
    paginate_by = 10
    template_name = 'tracksheet/assign_table.html'
    filterset_class = AssignFilter
    def get_queryset(self):
        queryset = ImageModel.objects.filter(assign_to=self.request.user)
        return queryset


class Project_Table(FilterView, ExportMixin, SingleTableView,PermissionRequiredMixin):
    permission_required = 'project.view_projects'
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

    def get_queryset(self):
        queryset = CheckoutModel.objects.filter(created_by = self.request.user).order_by('-created_at')
        return queryset


def get_current_path(request):
    current_url = request.get_full_path()
    return current_url
    #print (current_url)
    # return {
    #    'current_path': request.get_full_path()
    #  }


#####################################################################################
"""
items list
"""
class ItemListView(ListView):
    model = Checkout
    template_name = 'tracksheet/item_list.html'

    def get_queryset(self):
        return Checkout.objects.all()


class ItemUpdateView(UpdateView):
    model = Checkout
    form_class = CheckoutForm
    template_name = 'tracksheet/item_edit_form.html'

    def dispatch(self, *args, **kwargs):
        self.item_id = kwargs['pk']
        return super(ItemUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        item = Checkout.objects.get(id=self.item_id)
        return HttpResponse(render_to_string('tracksheet/item_edit_form_success.html', {'item': item}))



#####################################################################################










def checkoutimage(request,pk=None):
    qs = get_object_or_404(Image,pk = pk)
    icks = CheckoutModel.objects.filter(image_name = qs.image_name)
    print(icks)
    return render(request,'tracksheet/imagecheckout.html',{'icks':icks})


def get_check_date(request,pk):
    qs = get_object_or_404(CheckoutModel,pk=pk)
    return qs.checkin_at

def get_label_time(request,i_status,pk=None):
    instance = get_object_or_404(ImageModel, pk=pk)
    if i_status=='InProcess' or i_status=='Labelled':
        total_label_time = (CheckoutModel.objects.filter(Q(image_id__pk=instance.id),Q(image_status = "Labelled") | Q(image_status = "InProcess") ).aggregate(total=Sum('total_time'))['total'])
        #print (total_label_time)
        instance.label_time = total_label_time
        #instance.label_date = datetime.datetime.now().strftime("%Y-%m-%d")
        instance.label_by = str(request.user.first_name)
    elif i_status == 'ChangeNeeded' or i_status == 'InQuality' or i_status=='Corrected':
        total_correction_time = (CheckoutModel.objects.filter(Q(image_id__pk=instance.id),Q(image_status = "ChangeNeeded") | Q(image_status = "InQuality") | Q(image_status = "Corrected")).aggregate(total=Sum('total_time'))['total'])
        #print(total_correction_time)
        instance.correction_time = total_correction_time
        #instance.corrected_date = datetime.datetime.now().strftime("%Y-%m-%d")
        instance.corrected_by = str(request.user.first_name)
    elif i_status == 'Approved':
        instance.approved_by = str(request.user.first_name)
        instance.approved_date = datetime.datetime.now().strftime("%Y-%m-%d")

    chkinstance = CheckoutModel.objects.filter(image_id__pk=instance.id, image_status="ChangeNeeded").count()
    instance.loop_on_image = chkinstance
    instance.status = i_status
    instance.save()


#<QuerySet [<Group: Labeller>, <Group: Quality Check>, <Group: Quality2>, <Group: Team Lead>, <Group: Team Head>, <Group: Data analyst>, <Group: Employee>, <Group: Super Admin>, <Group: admin>]>
#checkin_instance = 0
# def check_field(request,checkout_id):
#     go = get_object_or_404(Checkout,Checkout.pk == checkout_id)
#     print (go)
#     if go.checkin_at == " ":
#         print ("null")


def editCheckout(request,pk=None):
    chkout = get_object_or_404(CheckoutModel,pk = pk)
    image_name = Checkout.get_image_name(chkout)
    project_name = Checkout.get_image_project(chkout)
    imageInstance = get_object_or_404(ImageModel,pk=chkout.image.id)

    if chkout.checkin_at != None:
        messages.error(request,"You cannot Edit Again!")
        return redirect('add_checkout',pk=imageInstance)
    #print (project_name)
    #project_name = get_object_or_404(ImageModel,image_name)
    if chkout.checkin_at is None:
        checkin_instance = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        checkin_instance = chkout.checkin_at

    form = CheckinForm(request.POST or None,initial={'image_id': chkout.image,'checkin_at':checkin_instance},instance=chkout)
    if form.is_valid():
        instance = form.save(commit=False)
        checkin = form.cleaned_data['checkin_at']
        checkout = form.cleaned_data['checkout_at']
        i_status = form.cleaned_data['image_status']
        # if i_status=='Corrected':
        #     imageInstance.layer_issues =instance.layer_issues
        #     imageInstance.border_issues = instance.border_issues
        #     imageInstance.missing_objects = instance.missing_objects
        if i_status == 'InProcess' or i_status == 'Labelled':
            imageInstance.label_date = instance.checkout_at.date()

        if i_status == 'ChangeNeeded' or i_status == 'InQuality' or i_status == 'Corrected':
            imageInstance.layer_issues = (instance.layer_issues)
            imageInstance.border_issues = (instance.border_issues)
            imageInstance.missing_objects = (instance.missing_objects)
            imageInstance.corrected_date = instance.checkout_at.date()
           # imageInstance.status=instance.status

        if checkin is not None:
            if checkin >= checkout:
                total_time = checkin-checkout
                days, seconds = total_time.days, total_time.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                instance.total_time = datetime.timedelta(days=days,hours=hours,minutes=minutes,seconds=seconds)
            else:
                messages.error(request,'enter Valid date-time')
                return redirect('edit_checkout', pk=pk)
        else:
            messages.error(request,'please insert checkin time')
            return redirect('edit_checkout', pk=pk)

        instance.created_by = request.user

        # if i_status == 'Labelled' or i_status == 'InProcess':
        #     ImageModel.label_by = request.user
        #     instance.save(commit = False)
        #     print("status",i_status)
        #     print("Label by", ImageModel.label_by)
        #
        # if i_status == 'Corrected' or i_status == 'ChangeNeeded' or i_status == 'InQuality' :
        #     ImageModel.corrected_by = request.user
        #     instance.save(commit=False)

        instance.save()
        imageInstance.total_objects = instance.image_objects
        imageInstance.save()
        get_label_time(request,i_status, pk=chkout.image.pk)
        #print(str(request.user.get_full_name()))
        messages.success(request, 'Checked In successful')
        return redirect('add_checkout', pk=imageInstance)

    context = {

        'id':chkout.image.pk,
        "instance": image_name,
        "form": form,
    }
    return render(request, 'tracksheet/editcheckout.html', context)

def addCheckout(request,pk=None):
    image = get_object_or_404(ImageModel, pk=pk)
    #print (image.image_name)
    checkout_instance = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    form = CheckoutForm(request.POST or None,initial={'image':image,'checkout_at':checkout_instance})
    checkout_of = CheckoutModel.objects.filter(image = image.id)
    table = CheckoutHistoryTable(checkout_of)
    RequestConfig(request,paginate={'per_page': 10}).configure(table)
    if form.is_valid():
        checkout_list = Checkout.objects.filter(created_by=request.user, checkin_at__isnull=True)
        if checkout_list:
            # error = messages.error(request, 'Please Make Sure Your Previous Checkout Are Done..')
            messages.warning(request, "Please Make Sure Your Previous Checkout Are Done..")
            return redirect('add_checkout',pk=pk)
        instance = form.save(commit=False)
        checkout = form.cleaned_data['checkout_at']
        #checkin = form.cleaned_data['checkin_at']
        i_status = form.cleaned_data['image_status']
        instance.created_by = request.user
        instance.image_id = image.id

        get_label_time(request,i_status,pk=pk)
        instance.save()
        messages.success(request, 'Checked Out successful')
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


def export(request, tarik):
    person_resource = ImageResource()
    today = datetime.datetime.today()
    a = (today.date())
    aj = str(a)
    print(aj)
    queryset = ImageModel.objects.filter(
        Q(corrected_date=tarik) | Q(label_date=tarik) | Q(created_at=tarik), ~Q(status='Unlabelled'))
    print(queryset)
    dataset = person_resource.export(queryset)
    #print(dataset)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tracksheet%s.xls"'%(aj)
    return response


# queryset = Person.objects.filter(location='Helsinki')
# dataset = person_resource.export(queryset)
@login_required
def myexport(request):
    if not request.user.is_superuser:
        return redirect ('/tracksheet')

    t = (request.GET.get('q'))
    if t:
        a = export(request, t)
        return a
    return render(request, 'tracksheet/export.html', {})