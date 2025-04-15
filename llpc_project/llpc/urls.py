from django.urls import path
from . import views

app_name = 'llpc'

urlpatterns = [
    path('', views.index, name='index'),
    path('laboratory/', views.laboratory_form, name='laboratory_form'),
    path('parameter-evaluation/', views.parameter_evaluation, name='parameter_evaluation'),
    path('evaluation-success/', views.evaluation_success, name='evaluation_success'),
    path('loinc-search/', views.loinc_search, name='loinc_search'),
] 