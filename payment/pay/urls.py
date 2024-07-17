from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stkpush/', views.stkPush, name='stkpush'),
    path('checkstatus/', views.checkStatus, name='checkstatus'),
    path('callback/', views.callback, name='callback')
]