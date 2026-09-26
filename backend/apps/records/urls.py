from django.urls import path
from . import views

urlpatterns = [
    path('', views.medical_records_view, name='medical_records'),
    path('delete/<int:pk>/', views.delete_medical_record, name='delete_medical_record'),
    path('export-pdf/', views.export_pdf_view, name='export_health_pdf'),
    path('export-pdf/<int:member_id>/', views.export_pdf_view, name='export_member_pdf'),
]
