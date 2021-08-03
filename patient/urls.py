from os import name
from patient.models import patient
from django.urls import path
from patient import views
from prediction import views as pred_views
from authorize import views as home_views

urlpatterns = [
    path('', views.patient, name='patient'),
    path('edit/<str:name><int:id>', views.edit, name='edit'),
    path('prediction/', pred_views.prediction, name='prediction/diagnosis.html'),
    path('homepage', home_views.homepage, name='authorize/homepage.html'),
]
