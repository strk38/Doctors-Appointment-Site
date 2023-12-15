
from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
import datetime
from django.template import context
from django.template.loader import render_to_string,get_template
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def SignUpPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1==pass2 :
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
        else:
            #messages.add_message(request, messages., f'Password doesnot match')
            return HttpResponse("Password doesnt match")    #HttpResponseRedirect(request.path)
        #print(uname,email,pass1,pass2)
        return render(request,'login.html')

    return  render(request,'signup.html')


def loginPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(username=uname,password=pass1)
        if user is not None:
            login(request,user)
            return render(request,'index.html')
        else:
            return HttpResponse("Invalid Username or Password")
    return  render(request,'login.html')

@login_required
def logoutPage(request):
    logout(request)
    return render(request,'index.html')


class HomeTemplateView(TemplateView):
    template_name= 'index.html'

    def post(self,request):

        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        #print(name, ' /// ',email, ' /// ',message)

        from_email=settings.EMAIL_HOST_USER
        message1='Dear '+name+', You have booked an appointment for '+message
        #print(message1)
        send_mail(
            "Wants to book appointment",
            message1,
            from_email,
            [email],
            fail_silently=False,
        )
        '''
        email = EmailMessage{
            subject=f'{name}, Wants to book appointment'
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        }
        email.send()
        '''
        messages.add_message(request, messages.SUCCESS, f'Mail Sent Successfully.')
        return render(request,'appointment.html') 

# Create your views here.
# def home(request):
#    return HttpResponse('Working') 
    #render(request,'home.html')

class AppointmentTemplateView(TemplateView):
    template_name= 'appointment.html'

    def post(self,request):
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        msg=request.POST.get('message')

        appointment=Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            message=msg,
        )
        appointment.save()

        messages.add_message(request, messages.SUCCESS, f'Appointment Booked Successfully')
        return HttpResponseRedirect(request.path)


class ManageAppointmentTemplateView(ListView):
    template_name= 'manage-appointments.html'
    model = Appointment
    context_object_name = "appointments"
    login_required=True
    paginate_by=3
    
    def post(self,request):
        date=request.POST.get('date')
        appointment_id=request.POST.get('appointment-id')
        appointment=Appointment.objects.get(id=appointment_id)
        appointment.accepted=True
        appointment.accepted_date=datetime.datetime.now()
        appointment.appointment_date=date
        appointment.save()

        data={
            'fname': appointment.first_name,
            'date': date,
        }
        message=get_template('email.html').render(data)
        '''
        send_mail(
            "Regarding Your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
            fail_silently=False,
        )
        '''
        email = EmailMessage(
            "Regarding Your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()


        messages.add_message(request, messages.SUCCESS, f'Appointment Accepted')
        return HttpResponseRedirect(request.path)

    def get_context_data(self, *args, **kwargs):
        context= super().get_context_data(*args, **kwargs)
        appointments=Appointment.objects.all()

        context.update({
            'title': 'Manage Appointments'
        })
        return context