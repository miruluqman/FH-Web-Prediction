from django.urls import path
from authorize import views
from django.contrib.auth import views as auth_views
from prediction import views as pred_views
from patient import views as pat_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.frontpage, name = 'frontpage'),
    path('login/', auth_views.LoginView.as_view(template_name='authorize/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('homepage/', views.homepage, name = 'homepage'),
    path('prediction/', pred_views.prediction, name = 'prediction/diagnosis.html'),
    path('patient/', pat_views.patient, name = 'patient/patient.html'),
    path('test/',views.test, name='test'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
