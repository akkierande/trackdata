# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from django.db import models
from django.urls import reverse
import datetime


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='employee')
    fullname = models.CharField(max_length=200, null=True)
    dob = models.DateField(null=True)
    department = models.CharField(max_length=100, null=True)
    previous_designation = models.CharField(max_length=100, null=True)
    designation = models.ForeignKey(Group, on_delete=models.CASCADE, default='7')
    shift = models.CharField(max_length=100, null=True)
    emp_id = models.IntegerField(null=True, default="00000")
    project = models.CharField(max_length=100, null=True)
    education = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=50, null=True)
    experience = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    def __str__(self):
        # return self.fullname
        if self.user.first_name != '' or self.user.last_name != '':
            return '{} {}'.format(self.user.first_name, self.user.last_name)
        else:
            return self.fullname


# Create your models here.
class Project(models.Model):
    Status = (
        ('Current', 'Current'),
        ('On Hold', 'On Hold'),
        ('Complete', 'Complete'),
        ('Planned', 'Planned'),
    )
    project_name = models.CharField(max_length=200)
    customer = models.CharField(max_length=200)
    project_type = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resources = models.IntegerField()
    total_image = models.IntegerField()
    current_uploaded = models.IntegerField()
    challenges = models.CharField(max_length=500)
    project_status = models.CharField(max_length=15, choices=Status, default="Planned")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    def __str__(self):
        return self.project_name


class Package(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('Label', 'Labelled'),
        ('Corrected', 'Corrected'),
        ('Uploaded', 'Uploaded'),
    )
    total_image = models.IntegerField(null=True, default="00000")
    package_name = models.CharField(max_length=200)
    package_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    def __str__(self):
        return self.package_name

class Image(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('Labelled', 'Labelled'),
        ('Corrected', 'Corrected'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
        ('Approved','Approved'),
        ('ChangeNeeded', 'ChangeNeeded'),
    )
    image_name = models.CharField(max_length=200)
    image_type = models.CharField(max_length=150)
    file_type = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    def __str__(self):
        return self.image_name


class Checkout(models.Model):
    Status = (
        ('InProcess', 'InProcess'),
        ('Labelled', 'Labelled'),
        ('Corrected', 'Corrected'),
        ('ChangeNeeded', 'ChangeNeeded'),
    )
    image_name = models.ForeignKey(Image,on_delete=models.CASCADE)
    image_objects = models.PositiveIntegerField(blank=True, null=True)
    image_status = models.CharField(max_length=15, choices=Status)
    checkout_at = models.DateTimeField(auto_created=True, null=True)
    checkin_at = models.DateTimeField(auto_created=True,null=True,blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    total_time = models.CharField(max_length=10,blank=True, null=True)

    def __str__(self):
        return str(self.image_name)

    def get_image_id(self):
        qs = Image.objects.get(image_name=self.image_name)
        image_id = qs.id
        return image_id

    def get_absolute_url(self):
        return reverse('image_id', kwargs={'pk': self.pk})

    # def get_total_time(self):
    #     total_time_on_image = 0
    #     checkout = Checkout.checkout_at
    #     checkin = Checkout.checkin_at
    #     if checkout and checkin:
    #         total_time_on_image = checkout - checkin
    #     return total_time_on_image

    get_latest_by = "checkout_at"