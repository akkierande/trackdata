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
        fields = ("username","password1","password2","first_name", "last_name", "email",)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CheckoutForm(forms.ModelForm):
    #helper.field_class = 'form-group'

    #checkout_at = forms.DateTimeField(widget=DateTimePicker(options={'format': '%Y-%m-%d %H:%M','language': 'en-us',}),)
    #checkout_at = forms.DateTimeField(required=False,widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))
    created = User.username
    class Meta:
        model = Checkout

        exclude = {
            'created_by'
        }
        widgets = {
            # Use localization and bootstrap 3
            'checkout_at': DateTimeWidget(attrs={'id': "checkout_at",'class':"form-control"}, usel10n=True, bootstrap_version=3),
            'checkin_at': DateTimeWidget(attrs={'id': "checkin_at",'class':"form-control"}, usel10n=True, bootstrap_version=3),
            'created_by': User.username,
            'image_id': widgets.Select(attrs={'class': "form-control"}),
            'image_objects':widgets.NumberInput(attrs={'class': "form-control"}),
            'image_status':widgets.Select(attrs={'class': "form-control"}),
            'comment':widgets.TextInput(attrs={'class': "form-control"}),
            'total_time':widgets.NumberInput(attrs={'class': "form-control"}),

        }


    # def created(model):
    #     created_by =User.USERNAME_FIELD
    #     return created_by




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







