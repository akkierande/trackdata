# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin import AdminSite
from .models import Project, Package, Image, Employee, Checkout


class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'total_image', 'project', 'package_status')
    search_fields = ('package_name', 'package_status')


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'image_status', 'checkout_at', 'time_on_image')
    search_fields = ('image_id', 'image_status')

# Register your models here.

admin.site.register(Project)
admin.site.register(Image)
admin.site.register(Employee)
admin.site.register(Package, PackageAdmin)
admin.site.register(Checkout, CheckoutAdmin)
