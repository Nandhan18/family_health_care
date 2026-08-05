from django.urls import path
from . import views

urlpatterns = [
    path('', views.emergency_view, name='emergency'),
]
