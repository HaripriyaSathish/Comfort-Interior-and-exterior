from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('enquiry/', views.submit_enquiry, name='submit_enquiry'),
]
