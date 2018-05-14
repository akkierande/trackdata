# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-02 12:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_at', models.DateTimeField(auto_created=True, blank=True, null=True)),
                ('checkout_at', models.DateTimeField(auto_created=True, null=True)),
                ('image_objects', models.PositiveIntegerField(blank=True, null=True)),
                ('layer_issues', models.IntegerField(blank=True, null=True)),
                ('border_issues', models.IntegerField(blank=True, null=True)),
                ('missing_objects', models.IntegerField(blank=True, null=True)),
                ('image_status', models.CharField(choices=[('InProcess', 'InProcess'), ('Labelled', 'Labelled'), ('Corrected', 'Corrected'), ('ChangeNeeded', 'ChangeNeeded'), ('InQuality', 'InQuality'), ('Approved', 'Approved')], max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('total_time', models.DurationField(blank=True, null=True)),
            ],
            options={
                'ordering': ['checkout_at'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='employee', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fullname', models.CharField(max_length=200, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('previous_designation', models.CharField(blank=True, max_length=100, null=True)),
                ('shift', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('project', models.CharField(blank=True, max_length=100, null=True)),
                ('education', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('experience', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=20)),
                ('updated_by', models.CharField(default='admin', max_length=20)),
                ('designation', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'permissions': (('view_employees', 'Can view employees'),),
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('completed_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('total_image', models.IntegerField(default='00000', null=True)),
                ('folder_name', models.CharField(max_length=200)),
                ('folder_date', models.DateField()),
                ('folder_status', models.CharField(choices=[('Unlabelled', 'Unlabelled'), ('InProcess', 'InProcess'), ('Completed', 'Completed'), ('Uploaded', 'Uploaded')], default='Unlabelled', max_length=15)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=20)),
                ('updated_by', models.CharField(default='admin', max_length=20)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('view_folder', 'Can view folder'),),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=200)),
                ('image_type', models.CharField(choices=[('hard', 'hard'), ('easy', 'easy'), ('medium', 'medium')], default='hard', max_length=150, null=True)),
                ('file_type', models.CharField(choices=[('png', 'png'), ('pgm', 'pgm'), ('ppm', 'ppm')], default='png', max_length=50)),
                ('status', models.CharField(choices=[('Unlabelled', 'Unlabelled'), ('InProcess', 'InProcess'), ('Labelled', 'Labelled'), ('Corrected', 'Corrected'), ('ChangeNeeded', 'ChangeNeeded'), ('InQuality', 'InQuality'), ('Approved', 'Approved'), ('Uploaded', 'Uploaded')], default='Unlabelled', max_length=15)),
                ('label_time', models.CharField(blank=True, max_length=10, null=True)),
                ('correction_time', models.CharField(blank=True, max_length=10, null=True)),
                ('loop_on_image', models.IntegerField(blank=True, null=True)),
                ('assign_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=20)),
                ('updated_by', models.CharField(default='admin', max_length=20)),
                ('assign_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Folder')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('completed_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('total_image', models.IntegerField(default='00000', null=True)),
                ('package_name', models.CharField(max_length=200)),
                ('package_date', models.DateField()),
                ('package_status', models.CharField(choices=[('Unlabelled', 'Unlabelled'), ('InProcess', 'InProcess'), ('Completed', 'Completed'), ('Uploaded', 'Uploaded')], default='Unlabelled', max_length=15)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=20)),
                ('updated_by', models.CharField(default='admin', max_length=20)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('view_package', 'Can view package'),),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('customer', models.CharField(max_length=200)),
                ('project_type', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('resources', models.IntegerField()),
                ('total_packages', models.IntegerField()),
                ('current_uploaded', models.IntegerField()),
                ('challenges', models.CharField(max_length=500)),
                ('project_status', models.CharField(choices=[('Current', 'Current'), ('On Hold', 'On Hold'), ('Complete', 'Complete'), ('Planned', 'Planned')], default='Planned', max_length=15)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=20)),
                ('updated_by', models.CharField(default='admin', max_length=20)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('view_projects', 'Can view projects'),),
            },
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('completed_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('total_image', models.IntegerField(default='00000', null=True)),
                ('sequence_name', models.CharField(max_length=200)),
                ('sequence_date', models.DateField()),
                ('sequence_status', models.CharField(choices=[('Unlabelled', 'Unlabelled'), ('InProcess', 'InProcess'), ('Completed', 'Completed'), ('Uploaded', 'Uploaded')], default='Unlabelled', max_length=15)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=20)),
                ('updated_by', models.CharField(default='admin', max_length=20)),
                ('folder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Folder')),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Package')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Project')),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('view_sequence', 'Can view sequence'),),
            },
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('completed_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('total_image', models.IntegerField(default='00000', null=True)),
                ('set_name', models.CharField(max_length=200)),
                ('set_date', models.DateField()),
                ('set_status', models.CharField(choices=[('Unlabelled', 'Unlabelled'), ('InProcess', 'InProcess'), ('Completed', 'Completed'), ('Uploaded', 'Uploaded')], default='Unlabelled', max_length=15)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='admin', max_length=20)),
                ('updated_by', models.CharField(default='admin', max_length=20)),
                ('folder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Folder')),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Package')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Project')),
                ('sequence', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Sequence')),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('view_set', 'Can view set'),),
            },
        ),
        migrations.AddField(
            model_name='package',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Project'),
        ),
        migrations.AddField(
            model_name='image',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Package'),
        ),
        migrations.AddField(
            model_name='image',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Project'),
        ),
        migrations.AddField(
            model_name='image',
            name='sequence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Sequence'),
        ),
        migrations.AddField(
            model_name='image',
            name='set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Set'),
        ),
        migrations.AddField(
            model_name='folder',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Package'),
        ),
        migrations.AddField(
            model_name='folder',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Project'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='checkout',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracksheet.Image'),
        ),
    ]
