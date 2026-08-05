from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicines_view, name='medicines'),
    path('delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
]
