from os import name
from django.urls import path, include
from prediction import views
from authorize import views as auth_views
from patient import views as pt_views

urlpatterns = [
    path('', views.prediction, name='prediction'),
    path('result/', views.result, name='result'),
    path('batch/', views.batch, name='batch'),
    path('home/', auth_views.homepage, name='authorize/homepage.html'),
    path('patient/', pt_views.patient, name='patient/patient.html'),
]
