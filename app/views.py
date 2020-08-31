# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import (TemplateView,FormView, RedirectView)
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import (User, Group) 
from django.contrib.auth import (login as auth_login, logout as auth_logout, authenticate)
from django.contrib import messages
from random import randint
from datetime import (date, timedelta, datetime) 
import calendar

from .models import *

# Create your views here.


class Index(TemplateView):
    template_name = "index.html"


""" Authentication views """


class Login(FormView):

    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        ctx = super(Login, self).get_context_data(**kwargs)

        ctx['rand'] = randint(100, 999)
  
        return ctx

    def post(self, request):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if request.user.is_superuser:
                    return HttpResponseRedirect('/super-admin')
                else:
                    return HttpResponseRedirect('/employee/'+str(user.id))
            else:
                messages.error(self.request,
                               "User is not Active")
                return HttpResponseRedirect('/')
        else:
            messages.error(self.request,
                           "User Does not Exist")
            return HttpResponseRedirect('/login')


class LogoutView(RedirectView):
    
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


""" Authentication Views End"""


""" Employee's Views """


class Home(LoginRequiredMixin, TemplateView):

    """
    Provides datails about employee's leaves
    """

    login_url = '/login/'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        employee = EmployeeDetails.objects.get(name=user.username)
        leaves = LeaveApplication.objects.filter(
            employee=employee.id).order_by('-date')

        # check if the employee exeeds the leave limit
        if employee.no_of_remaining_leaves == 0:
            ctx['application_closed'] = True
            ctx['message'] = 'Your maximum leave is completed'
        else:
            ctx['application_closed'] = False
        print('Leaves', employee.no_of_applied_leaves)

        if employee.no_of_applied_leaves >= 18:
            ctx['application_closed'] = True
            ctx['message'] = 'Your maximum leave to be apply is completed'

        ctx['employee_name'] = employee.name
        ctx['no_of_leaves'] = employee.no_of_leaves
        ctx['no_of_remaining_leaves'] = employee.no_of_remaining_leaves
        ctx['total_leaves'] = employee.total_no_of_leaves
        ctx['leaves_list'] = []

        for leave in leaves:
            print('status', leave.status)
            data = {}
            if leave.status == 'Not Approved':
                data['show_delete_button'] = True
            elif leave.status == 'Approved':
                data['show_delete_button'] = False
            data['id'] = leave.id
            data['leave_type'] = leave.leave_type
            data['date'] = leave.date
            data['duration'] = leave.duration
            data['status'] = leave.status

            ctx['leaves_list'].append(data)

        # Create a random intiger 
        ctx['rand'] = randint(100, 999)

        return ctx


class ApplyLeave(FormView):
    """ View for apply leave """
    def post(self, request):
        
        levae_type = self.request.POST.get('levae_type')
        duration = self.request.POST.get('DurationRadioOptions')
        date = self.request.POST.get('date')
        start_date = self.request.POST.get('start_date')
        end_date = self.request.POST.get('end_date')
        reason = self.request.POST.get('reason')

        employee = EmployeeDetails.objects.get(name=request.user)

        if len(start_date) > 0:

            date1 = datetime.strptime(start_date, '%m/%d/%Y')
            date2 = datetime.strptime(end_date, '%m/%d/%Y')

            delta = date2 - date1

            for i in range(delta.days + 1):
                days = date1 + timedelta(days=i)

                leave = LeaveApplication()

                week_day = calendar.day_name[
                    datetime.strptime(
                        str(days), '%Y-%m-%d %H:%M:%S'
                        ).weekday()] 

                if week_day != 'Saturday' and week_day != 'Sunday':

                    if int(employee.no_of_applied_leaves) <= 17:

                        employee.no_of_applied_leaves = float(employee.no_of_applied_leaves) + 1
                        employee.save()

                        leave.date = datetime.strptime(str(days), '%Y-%m-%d %H:%M:%S')
                        leave.leave_type = levae_type
                        leave.duration = 'Full Day'
                        leave.employee = employee
                        leave.description = reason

                        leave.save()

        elif len(start_date) == 0:
            leave = LeaveApplication()

            date = datetime.strptime(date, '%m/%d/%Y')

            week_day = calendar.day_name[date.weekday()] 

            if week_day != 'Saturday' and week_day != 'Sunday':

                if int(employee.no_of_applied_leaves) <= 17:

                    if duration == 'Full Day':
                        employee.no_of_applied_leaves = float(employee.no_of_applied_leaves) + 1
                    elif duration == 'Half Day':
                        employee.no_of_applied_leaves = float(employee.no_of_applied_leaves) + 0.5
                    employee.save()

                    leave.date = date
                    leave.leave_type = levae_type
                    leave.duration = duration
                    leave.employee = employee
                    leave.description = reason

                    leave.save()

        return HttpResponseRedirect('/employee/'+str(request.user.id))


class DeleteLeaveApplication(LoginRequiredMixin, RedirectView):
    """ To delete appllied leaves """
    login_url = '/login/'

    def get_redirect_url(self, *args, **kwargs):

        user_id = self.request.user.id
        username = self.request.user.username

        url = '/employee/' + str(user_id)  # Redirect url

        id = kwargs['pk']  # Leave id
        
        employee = EmployeeDetails.objects.get(name=username)
        leave = LeaveApplication.objects.get(id=id)

        duration = leave.duration
        
        if duration == 'Half Day':
                employee.no_of_applied_leaves = float(employee.no_of_applied_leaves) - 0.5
        if duration == 'Full Day':
                employee.no_of_applied_leaves = float(employee.no_of_applied_leaves) - 1

        employee.save()
        leave.delete()  # Delete leave application
        
        return url


""" Employee's Views End """

""" Super Admin Views """ 


class SuperAdmin(LoginRequiredMixin, TemplateView):

    """
    View for super user with privileges
    """

    login_url = '/login/'
    redirect_field_name = '/super-admin/'
    template_name = 'superadmin.html'

    def get_context_data(self, **kwargs):
        ctx = super(SuperAdmin, self).get_context_data(**kwargs)

        leaves = LeaveApplication.objects.all().order_by('-date')
   
        ctx['username'] = self.request.user
        ctx['leaves'] = leaves
        ctx['rand'] = randint(100, 999)
  
        return ctx


class SaveLeaveStatus(LoginRequiredMixin, RedirectView):
    """ View to approve leaves """
    login_url = '/login/'
    url = '/super-admin'

    def get_redirect_url(self, *args, **kwargs):
        
        id = kwargs['pk']
        status = self.request.GET.get('status')
        employee_name = self.request.GET.get('employee')
        duration = self.request.GET.get('duration')

        leave = LeaveApplication.objects.get(id=id)
        employee = EmployeeDetails.objects.get(name=employee_name)

        leave.status = status
        leave.save()

        if status is not None:
            if status == 'Approved':
                if duration == 'Half Day':
                    employee.no_of_leaves = float(employee.no_of_leaves) + 0.5
                    employee.no_of_remaining_leaves = float(employee.no_of_remaining_leaves) - 0.5
                elif duration == 'Full Day':
                    employee.no_of_leaves = float(employee.no_of_leaves) + 1
                    employee.no_of_remaining_leaves = float(employee.no_of_remaining_leaves) - 1
            elif status == 'Not Approved':
                if duration == 'Half Day':
                    employee.no_of_leaves = float(employee.no_of_leaves) - 0.5
                    employee.no_of_remaining_leaves = float(employee.no_of_remaining_leaves) + 0.5
                elif duration == 'Full Day':
                    employee.no_of_leaves = float(employee.no_of_leaves) - 1
                    employee.no_of_remaining_leaves = float(employee.no_of_remaining_leaves) + 1
        employee.save()
        return super(SaveLeaveStatus, self).get_redirect_url(*args, **kwargs)





