from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointments_view, name='appointments'),
    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),
]
