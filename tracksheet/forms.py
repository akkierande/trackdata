import datetime
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Checkout,Image,Employee
from datetimewidget.widgets import DateTimeWidget

from django import forms
from django.forms import widgets


from django.views.generic.detail import DetailView
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.



class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ("username","password1","password2","first_name", "last_name","email")
        # widgets = {
        #     # Use localization and bootstrap 3
        #     'username': widgets.TextInput,
        #     'first_name': widgets.TextInput,
        #     'last_name': widgets.TextInput,
        #     'email': widgets.EmailInput,
        #     'password1': widgets.PasswordInput,
        #     'password2': widgets.PasswordInput,
        # }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CheckoutForm(forms.ModelForm):
    field_order = ['image_name','image_status','checkout_at','checkin_at']

    class Meta:
        model = Checkout
        #created = User.username
        exclude = {
            'created_by',
            'total_time',
        }
        dateTimeOptions = {
            'autoclose': True,
        }

        widgets = {
            # Use localization and bootstrap 3
            'checkout_at': widgets.TextInput(attrs={'class': "form-control",'readonly': True,}),
            'checkin_at': DateTimeWidget(options=dateTimeOptions,attrs={'id': "checkin_at",'class':"form-control",'placeholder':"Image Stop Time"}, usel10n=True, bootstrap_version=3),
            'image_name': widgets.Select(attrs={'class': "form-control disabled"}),
            'image_objects':widgets.NumberInput(attrs={'class': "form-control","min":"0",'placeholder':"Total Objects In Image"}),
            'image_status':widgets.Select(attrs={'class': "form-control"}),
            'comment':widgets.TextInput(attrs={'class': "form-control",'placeholder':"Put Your Comment Here"}),
            'total_time':widgets.NumberInput(attrs={'class': "form-control"}),
        }


    # def created(model):
    #     created_by =User.USERNAME_FIELD
    #     return created_by
    #     widgets = {
    #         'start_date': forms.DateInput(attrs={
    #             'class': 'datepicker', 'data-min': YOUR_MIN_DATE,
    #             'data-max': YOUR_MAX_DATE}),
    #     }



    # renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")



# def clean_renewal_date(self):
#     data = self.cleaned_data['renewal_date']
#
#     # Check date is not in past.
#     if data < datetime.date.today():
#         raise ValidationError(_('Invalid date - renewal in past'))
#
#     # Check date is in range librarian allowed to change (+4 weeks).
#     if data > datetime.date.today() + datetime.timedelta(weeks=4):
#         raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
#
#     # Remember to always return the cleaned data.
#     return data

#
# class ImageViewForm(forms.ModelForm):
#     #renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
#     class Meta:
#         model = Image
#         fields = '__all__'
#         # checkout_by = Employee.user
#         # exclude = {
#         #     'labelled_at'
#         # }
#     def save(self, commit=True):
#         image = super(ImageViewForm.Form, self).save(commit=False)
#         # checkout.comment = self.cleaned_data["comment"]
#
#         if commit:
#             image.save()
#         return image







