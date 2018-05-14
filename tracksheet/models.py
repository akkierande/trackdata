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
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,primary_key=True,related_name='employee')
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
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    resources = models.PositiveIntegerField(blank=True, null=True)
    total_packages = models.PositiveIntegerField(blank=True, null=True)
    current_uploaded = models.PositiveIntegerField(blank=True, null=True)
    challenges = models.CharField(max_length=500,blank=True, null=True)
    project_status = models.CharField(max_length=15, choices=Status, default="Planned")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=False, default="admin")
    updated_by = models.CharField(max_length=100, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_projects", "Can view projects"),
        )
        ordering = ['-id']

    def __str__(self):
        return self.project_name


class Package(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
    )
    State = (
        ('rework', 'rework'),
        ('practice', 'practice'),
    )
    total_image = models.PositiveIntegerField(null=True, default="00000")
    package_name = models.CharField(max_length=200)
    package_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    package_state = models.CharField(max_length=15, choices=State,null=True,blank=True)
    created_by = models.CharField(max_length=100, null=False, default="admin")
    updated_by = models.CharField(max_length=100, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_package", "Can view package"),
        )
        ordering = ['-id']
        unique_together=(('package_name','project'),)

    def __str__(self):
        return self.package_name

class Folder(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
    )
    total_image = models.PositiveIntegerField(null=True, default="00000")
    folder_name = models.CharField(max_length=200)
    folder_date = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    folder_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=False, default="admin")
    updated_by = models.CharField(max_length=100, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_folder", "Can view folder"),
        )
        ordering = ['-id']

    def __str__(self):
        return self.folder_name

class Sequence(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
    )
    total_image = models.PositiveIntegerField(null=True, default="00000")
    sequence_name = models.CharField(max_length=200)
    sequence_date = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    sequence_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=False, default="admin")
    updated_by = models.CharField(max_length=100, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_sequence", "Can view sequence"),
        )
        ordering = ['-id']

    def __str__(self):
        return self.sequence_name



class Set(models.Model):
    Status = (
        ('Unlabelled', 'Unlabelled'),
        ('InProcess', 'InProcess'),
        ('Completed', 'Completed'),
        ('Uploaded', 'Uploaded'),
    )
    total_image = models.PositiveIntegerField(null=True, default="00000")
    set_name = models.CharField(max_length=200)
    set_date = models.DateField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    set_status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    completed_date = models.DateField(auto_created=True, blank=True, null=True)
    uploaded_date = models.DateField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=False, default="admin")
    updated_by = models.CharField(max_length=100, null=False, default="admin")

    class Meta:
        permissions = (
            ("view_set", "Can view set"),
        )
        ordering = ['-id']

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
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, null=True,blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True,blank=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, null=True,blank=True)
    assign_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='image_assign_to')
    checked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='image_checked_by')
    status = models.CharField(max_length=15, choices=Status, default="Unlabelled")
    label_by = models.CharField(max_length=100, blank=True, null=True)
    label_time = models.CharField(max_length=20, blank=True, null=True)
    label_date = models.CharField(max_length=20, blank=True, null=True)
    corrected_by = models.CharField(max_length=100, blank=True, null=True)
    correction_time = models.CharField(max_length=20,blank=True, null=True)
    corrected_date = models.CharField(max_length=20,blank=True, null=True)
    total_objects = models.PositiveIntegerField(blank=True, null=True)
    approved_by = models.CharField(max_length=100,blank=True, null=True)
    approved_date = models.CharField(max_length=20,blank=True, null=True)
    loop_on_image = models.IntegerField(blank=True, null=True)
    assign_at = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=False, default="admin")
    updated_by = models.CharField(max_length=100, null=False, default="admin")
    layer_issues = models.PositiveIntegerField(blank=True, null=True)
    border_issues = models.PositiveIntegerField(blank=True, null=True)
    missing_objects = models.PositiveIntegerField(blank=True, null=True)
    remark = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        permissions = (
            ("view_image", "Can view image"),
        )
        ordering = ['-id']

    # def get_image_name(self):
    #     return self.image_name

class Checkout(models.Model):
    Status = (
        ('InProcess', 'InProcess'),
        ('Labelled', 'Labelled'),
        ('Corrected', 'Corrected'),
        ('ChangeNeeded', 'ChangeNeeded'),
        ('InQuality', 'InQuality'),
        ('InChecking', 'InChecking'),
        ('Checked', 'Checked'),
        ('Practice','Practice'),
        ('Approved', 'Approved'),
    )
    scene_type = (
        ('Country Road', 'Country Road'),
        ('Highway', 'Highway'),
        ('City', 'City'),
    )
    weather = (
        ('Clear', 'Clear'),
        ('Cloudy', 'Cloudy'),
        ('Rainy', 'Rainy'),
    )
    day_lights = (
        ('Day', 'Day'),
        ('Night', 'Night'),
        ('Twilight', 'Twilight'),
    )
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    image_objects = models.PositiveIntegerField(blank=True, null=True)
    scene_type = models.CharField(max_length=15,blank=True, null=True, choices=scene_type)
    weather = models.CharField(max_length=15,blank=True, null=True, choices=weather)
    day_lights = models.CharField(max_length=15,blank=True, null=True, choices=day_lights)
    no_of_scooters = models.PositiveIntegerField(blank=True, null=True)
    scooter_group = models.PositiveIntegerField(blank=True, null=True)
    no_of_motorbike = models.PositiveIntegerField(blank=True, null=True)
    motorbike_group = models.PositiveIntegerField(blank=True, null=True)
    no_of_bicycle = models.PositiveIntegerField(blank=True, null=True)
    no_of_mistakes = models.PositiveIntegerField(blank=True, null=True)
    bicycle_group = models.PositiveIntegerField(blank=True, null=True)
    layer_issues = models.PositiveIntegerField(blank=True, null=True)
    border_issues = models.PositiveIntegerField(blank=True, null=True)
    missing_objects = models.PositiveIntegerField(blank=True, null=True)
    other_tag_issues = models.PositiveIntegerField(blank=True, null=True)
    occlusion_truncation_issues = models.PositiveIntegerField(blank=True, null=True)
    total_unique_bicycle = models.PositiveIntegerField(blank=True, null=True)
    total_unique_scooter = models.PositiveIntegerField(blank=True, null=True)
    total_unique_motorbike = models.PositiveIntegerField(blank=True, null=True)
    total_unique_objects = models.PositiveIntegerField(blank=True, null=True)
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

    def get_image_project(self,pk=None):
        qs = Image.objects.get(id=self.image.id)
        project_name = qs.project
        return project_name

    def get_absolute_url(self):
        return reverse('image_id', kwargs={'pk': self.pk})

    get_latest_by = "checkout_at"

    class Meta:
        ordering = ['checkout_at']