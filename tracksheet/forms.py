import datetime
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Checkout,Image,Employee,Project
from datetimewidget.widgets import DateTimeWidget

from django import forms
from django.forms import widgets



class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ("username","password1","password2","first_name", "last_name","email")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CheckoutForm(forms.ModelForm):
    #image_name = Checkout.get_image_name
    field_order = ['image_id','image_status','checkout_at','checkin_at']

    class Meta:
        model = Checkout
        #created = User.username
        exclude = {
            'created_by',
            'total_time',
            'image',
        }
        dateTimeOptions = {

        }

        widgets = {
            # Use localization and bootstrap 3
            'image_id': widgets.TextInput(attrs={'class': "form-control disabled"}),
            'checkout_at': widgets.TextInput(attrs={'class': "form-control",'readonly': True,}),
            'checkin_at': DateTimeWidget(options=dateTimeOptions,attrs={'id': "checkin_at",'class':"form-control",'placeholder':"Image Stop Time"}, usel10n=True, bootstrap_version=3),
            'image_objects':widgets.NumberInput(attrs={'class': "form-control","min":"0",'placeholder':"Total Objects In Image"}),
            'image_status':widgets.Select(attrs={'class': "form-control"}),
            'comment':widgets.TextInput(attrs={'class': "form-control",'placeholder':"Put Your Comment Here"}),
            'total_time':widgets.NumberInput(attrs={'class': "form-control"}),
        }


class ProjectListForm(forms.ModelForm):
    project_name = forms.ModelChoiceField(queryset=Project.objects.filter())
    class Meta:
        model = Project
        fields = ("project_name",)
        widgets = {
            'project_name': widgets.Select(attrs={'onchange': 'refresh();'}),
        }



class EmployeeDetailForm(forms.Form):
    dob = forms.DateField()
    department = forms.CharField()
    previous_designation = forms.CharField()
    shift = forms.CharField()
    emp_id = forms.IntegerField()
    project = forms.CharField()
    education = forms.CharField()
    location = forms.CharField()
    experience = forms.CharField()

    dateTimeOptions = {
        'autoclose': True,
    }
    widgets = {
        # Use localization and bootstrap 3
        'dob': DateTimeWidget(options=dateTimeOptions,attrs={'id': "checkin_at",'class':"form-control",'placeholder':"Image Stop Time"}, usel10n=True, bootstrap_version=3),
        'department': widgets.TextInput(attrs={'class': "form-control" }),
        'previous_designation':widgets.TextInput( attrs={'id': "checkin_at", 'class': "form-control",
                                                                     'placeholder': "Image Stop Time"}),
        'shift': widgets.NumberInput(
            attrs={'class': "form-control", "min": "0", 'placeholder': "Total Objects In Image"}),
        'emp_id': widgets.Select(attrs={'class': "form-control"}),
        'education': widgets.TextInput(attrs={'class': "form-control", 'placeholder': "Put Your Comment Here"}),
        'location': widgets.NumberInput(attrs={'class': "form-control"}),
    }

    def clean(self):
        cleaned_data = super(EmployeeDetailForm, self).clean()
        dob = cleaned_data.get('dob')
        department = cleaned_data.get('department')
        shift = cleaned_data.get('shift')
        emp_id = cleaned_data.get('emp_id')
        project = cleaned_data.get('project')
        education = cleaned_data.get('education')
        location = cleaned_data.get('location')
        experience = cleaned_data.get('experience')

        if not dob and not department and not shift and not emp_id and not project and not education and not location and not experience:
            raise forms.ValidationError('You have to write All Fields!')

