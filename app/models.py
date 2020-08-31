# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.




class Leave(models.Model):
	total_leaves = models.PositiveIntegerField( default=18)

	def __str__(self):
		return str(self.total_leaves)


class EmployeeDetails(models.Model):
	name = models.CharField(max_length=100, blank=True, null=True, unique=True)
	no_of_leaves = models.FloatField( default=0)
	no_of_remaining_leaves = models.FloatField( default=18)
	no_of_applied_leaves = models.FloatField( default=0)
	total_no_of_leaves = models.FloatField(default=18)

	def __str__(self):
		return str(self.name)


class LeaveApplication(models.Model):

	STATUS = [
		("Not Approved", 'Not Approved'),
		("Approved", "Approved"),
	]

	LEAVE_TYPE = [
		("Casual Leave", 'Casual Leave'),
		("Sick Leave", "Sick Leave"),
	]

	DURATION = [
		("FULL Day", 'Full Day'),
		("Half Day", "Half Day"),
	]

	date = models.DateField('Date', null=True, blank=True)
	leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE, default='Casual Leave')
	duration = models.CharField(max_length=20, choices=DURATION, default='Full Day')
	employee = models.ForeignKey(EmployeeDetails, related_name = 'employee', on_delete=models.CASCADE, null=True)
	description = models.CharField(max_length=100, blank=True, null=True)
	status = models.CharField(max_length=20, choices=STATUS, default='Not Approved')

	def __str__(self):
		return str(self.duration)