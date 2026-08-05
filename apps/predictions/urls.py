from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_predictions_view, name='ai_predictions'),
]
