# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

# Register your models here.

class LeaveApplicationAdmin(admin.ModelAdmin):
	list_display = ['employee', 'date','leave_type','duration','status']

admin.site.register(Leave)
admin.site.register(EmployeeDetails)
admin.site.register(LeaveApplication, LeaveApplicationAdmin)
