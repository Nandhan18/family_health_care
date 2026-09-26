from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin Portal Routes
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-dashboard/user/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('admin-dashboard/user/<int:user_id>/toggle-staff/', views.admin_toggle_staff_view, name='admin_toggle_staff'),
    path('admin-dashboard/user/<int:user_id>/toggle-active/', views.admin_toggle_active_view, name='admin_toggle_active'),
    path('admin-dashboard/user/<int:user_id>/reset-password/', views.admin_reset_password_view, name='admin_reset_password'),
    path('admin-dashboard/create-user/', views.admin_create_user_view, name='admin_create_user'),
    path('admin-dashboard/user/<int:user_id>/delete/', views.admin_delete_user_view, name='admin_delete_user'),
]

