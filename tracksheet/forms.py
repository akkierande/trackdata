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
    field_order = ['image_id','image_status','checkout_at']

    class Meta:
        model = Checkout
        #created = User.username
        exclude = {
            'created_by',
            'total_time',
            'image',
            'checkin_at',
            'layer_issues',
            'missing_objects',
            'border_issues',
            'label_by',
            'correct_by',
            'scene_type',
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
            'total_unique_objects',
        }
        dateTimeOptions = {

        }

        widgets = {
            # Use localization and bootstrap 3
            'image_id': widgets.TextInput(attrs={'class': "form-control disabled"}),
            'checkout_at': widgets.TextInput(attrs={'class': "form-control",'readonly': True,}),
            #'checkin_at': DateTimeWidget(options=dateTimeOptions,attrs={'id': "checkin_at",'class':"form-control",'placeholder':"Image Stop Time"}, usel10n=True, bootstrap_version=3),
            'image_objects':widgets.NumberInput(attrs={'class': "form-control","min":"0",'placeholder':"Total Objects In Image"}),
            'image_status':widgets.Select(attrs={'class': "form-control"}),
            'comment':widgets.TextInput(attrs={'class': "form-control",'placeholder':"Put Your Comment Here"}),
            'total_time':widgets.NumberInput(attrs={'class': "form-control"}),
        }



class CheckinForm(forms.ModelForm):
    #image_name = Checkout.get_image_name
    field_order = ['image_id','image_status','checkout_at','checkin_at']

    class Meta:
        model = Checkout
        #created = User.username
        exclude = {
            'created_by',
            'total_time',
            'image',
            'label_by',
            'correct_by',
            'scene_type',
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
            'total_unique_objects',

        }
        dateTimeOptions = {

        }

        widgets = {
            # Use localization and bootstrap 3
            'image_id': widgets.TextInput(attrs={'class': "form-control disabled"}),
            'checkout_at': widgets.TextInput(attrs={'class': "form-control",'readonly': True,}),
            'checkin_at': widgets.TextInput(attrs={'class': "form-control", 'readonly': True, }),

            #'checkin_at': DateTimeWidget(options=dateTimeOptions,attrs={'id': "checkin_at",'class':"form-control",'placeholder':"Image Stop Time",'readonly': True,}, usel10n=True, bootstrap_version=3),
            'image_objects':widgets.NumberInput(attrs={'class': "form-control","min":"0",'placeholder':"Total Objects In Image"}),

            'layer_issues': widgets.NumberInput(
                attrs={'id':"layer_issues",'class': "form-control", "min": "0", 'placeholder': "Total Layer Issues In Image"}),
            'border_issues': widgets.NumberInput(
                attrs={'id':"border_issues",'class': "form-control", "min": "0", 'placeholder': "Total Border Issues In Image"}),
            'missing_objects': widgets.NumberInput(
                attrs={'id':"missing_objects",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),

            'image_status':widgets.Select(attrs={'class': "form-control"}),
            'comment':widgets.TextInput(attrs={'class': "form-control",'placeholder':"Put Your Comment Here"}),
            'total_time':widgets.NumberInput(attrs={'class': "form-control"}),
            'scene_type':widgets.Select(attrs={'class': "form-control",'id':"scene_type"}),
            'weather':widgets.Select(attrs={'class': "form-control",'id':"weather"}),
            'day_lights':widgets.Select(attrs={'class': "form-control",'id':"day_lights"}),
            'no_of_scooters':widgets.NumberInput(
                attrs={'id':"no_of_scooters",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'scooter_group':widgets.NumberInput(
                attrs={'id':"scooter_group",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'no_of_motorbike':widgets.NumberInput(
                attrs={'id':"no_of_motorbike",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'motorbike_group':widgets.NumberInput(
                attrs={'id':"motorbike_group",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'no_of_bicycle':widgets.NumberInput(
                attrs={'id':"no_of_bicycle",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'no_of_mistakes':widgets.NumberInput(
                attrs={'id':"no_of_mistakes",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'bicycle_group':widgets.NumberInput(
                attrs={'id':"bicycle_group",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'other_tag_issues':widgets.NumberInput(
                attrs={'id':"other_tag_issues",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'occlusion_truncation_issues':widgets.NumberInput(
                attrs={'id':"occlusion_truncation_issues",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'total_unique_bicycle':widgets.NumberInput(
                attrs={'id':"total_unique_bicycle",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'total_unique_scooter':widgets.NumberInput(
                attrs={'id':"total_unique_scooter",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'total_unique_motorbike':widgets.NumberInput(
                attrs={'id':"total_unique_motorbike",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
            'total_unique_objects':widgets.NumberInput(
                attrs={'id':"total_unique_objects",'class': "form-control", "min": "0", 'placeholder': "Total Missing Objects In Image"}),
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

