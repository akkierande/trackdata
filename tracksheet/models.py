# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group ,AbstractUser
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from datetime import datetime,time


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='employee')
    fullname = models.CharField(max_length=200, null=True)
    dob = models.DateField(null=True,blank=True)
    department = models.CharField(max_length=100, null=True,blank=True)
    previous_designation = models.CharField(max_length=100, null=True , blank=True)
    designation = models.ForeignKey(Group, on_delete=models.CASCADE, default='1')
    shift = models.CharField(max_length=100, null=True , blank=True)
    emp_id = models.IntegerField(blank=True,unique=True,null=True)
    project = models.CharField(max_length=100, null=True , blank=True)
    education = models.CharField(max_length=100, null=True , blank=True)
    location = models.CharField(max_length=50, null=True , blank=True)
    experience = models.CharField(max_length=100, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_employees", "Can view employees"),
        )

    def __str__(self):
        # return self.fullname
        return str(self.fullname)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.employee.save()


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
    total_packages = models.IntegerField()
    current_uploaded = models.IntegerField()
    challenges = models.CharField(max_length=500)
    project_status = models.CharField(max_length=15, choices=Status, default="Planned")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_projects", "Can view projects"),
        )

    def __str__(self):
        return self.project_name


class Package(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
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

    class Meta:
        permissions = (
            ("view_package", "Can view package"),
        )


    def __str__(self):
        return self.package_name

class Folder(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
    )
    total_image = models.IntegerField(null=True, default="00000")
    folder_name = models.CharField(max_length=200)
    folder_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    folder_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_folder", "Can view folder"),
        )

    def __str__(self):
        return self.folder_name

class Sequence(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
    )
    total_image = models.IntegerField(null=True, default="00000")
    sequence_name = models.CharField(max_length=200)
    sequence_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    sequence_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_sequence", "Can view sequence"),
        )

    def __str__(self):
        return self.sequence_name



class Set(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
    )
    total_image = models.IntegerField(null=True, default="00000")
    set_name = models.CharField(max_length=200)
    set_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    set_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_set", "Can view set"),
        )

    def __str__(self):
        return self.set_name


class Image(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Labelled', 'Labelled'),
        ('Corrected', 'Corrected'),
        ('ChangeNeeded', 'ChangeNeeded'),
        ('InQuality', 'InQuality'),
        ('Approved', 'Approved'),
        ('Uploaded', 'Uploaded'),
    )
    Image_type = (
        ('hard', 'hard'),
        ('easy', 'easy'),
        ('medium', 'medium'),
    )
    File_type = (
        ('png', 'png'),
        ('pgm', 'pgm'),
        ('ppm', 'ppm'),
    )
    image_name = models.CharField(max_length=200)
    image_type = models.CharField(max_length=150,choices=Image_type, default="hard",null=True)
    file_type = models.CharField(max_length=50,choices=File_type, default="png")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, null=True)
    assign_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    label_time = models.CharField(max_length=10, blank=True, null=True)
    correction_time = models.CharField(max_length=10,blank=True, null=True)
    loop_on_image = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=20, null=False, default="admin")
    updated_by = models.CharField(max_length=20, null=False, default="admin")

    def __str__(self):
        return str(self.pk)

    # def get_image_name(self):
    #     return self.image_name

class Checkout(models.Model):
    Status = (
        ('InProcess', 'InProcess'),
        ('Labelled', 'Labelled'),
        ('Corrected', 'Corrected'),
        ('ChangeNeeded', 'ChangeNeeded'),
        ('InQuality', 'InQuality'),
        ('Approved', 'Approved'),
    )
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    image_objects = models.PositiveIntegerField(blank=True, null=True)
    image_status = models.CharField(max_length=15, choices=Status)
    checkout_at = models.DateTimeField(auto_created=True, null=True)
    checkin_at = models.DateTimeField(auto_created=True,null=True,blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    total_time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    def get_image_name(self,pk = None):
        qs = Image.objects.get(id = self.image.id)
        image_name = qs.image_name
        return image_name

    def get_absolute_url(self):
        return reverse('image_id', kwargs={'pk': self.pk})

    get_latest_by = "checkout_at"