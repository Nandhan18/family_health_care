from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_analytics_view, name='health_analytics'),
    path('delete/<int:pk>/', views.delete_health_metric, name='delete_health_metric'),
]
