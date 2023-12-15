from django.urls import path,include
from . import views as vw
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView     #calling class from view.py (doctor)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',HomeTemplateView.as_view(), name='home'),
    path('sign-up/',vw.SignUpPage, name='signup'),
    path('login/',vw.loginPage, name='login'),
    path('make-appointment/',AppointmentTemplateView.as_view(), name='appointment'),
    path('manage-appointment/',login_required(ManageAppointmentTemplateView.as_view()), name='manage'),
    path('logout/',vw.logoutPage, name='logout'),
]
