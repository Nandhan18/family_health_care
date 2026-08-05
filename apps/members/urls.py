from django.urls import path
from . import views

urlpatterns = [
    path('', views.family_members_view, name='family_members'),
    path('delete/<int:pk>/', views.delete_family_member, name='delete_family_member'),
]
