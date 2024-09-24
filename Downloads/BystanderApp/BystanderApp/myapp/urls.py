from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name="landingpage"),
    path('reg/', views.register, name="registration"),
    path('login/', views.login_view, name="login"),
    path('pdash/', views.patientdash, name="patient_dashboard"),
    path('bdash/', views.bystanderdash, name="bystander_dashboard"),
    path('log/', views.logout, name="logout"),
    path('pro/', views.profile, name='profilemanagement'),
    path('medhis/', views.medicalhistory, name="medical_history"),
]
