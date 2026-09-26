from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from functools import wraps

from apps.members.models import FamilyMember
from apps.records.models import MedicalRecord
from apps.medicines.models import Medication
from apps.appointments.models import Appointment
from .forms import CustomUserCreationForm

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in with administrator credentials.")
            return redirect('admin_login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access Denied: Administrator privileges are required.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def landing_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    return render(request, 'landing.html')

def signup_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Family Care, {user.first_name}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff or user.is_superuser:
                messages.success(request, f"Welcome back, Administrator {user.first_name or user.username}!")
                return redirect('admin_dashboard')
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    response = render(request, 'auth/login.html', {'form': form})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def admin_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not (user.is_staff or user.is_superuser):
                messages.error(request, "Access Denied: Account does not have administrator permissions.")
                return render(request, 'auth/admin_login.html', {'form': form})
            login(request, user)
            messages.success(request, f"Welcome to Admin Portal, {user.first_name or user.username}!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid administrator credentials.")
    else:
        form = AuthenticationForm()

    response = render(request, 'auth/admin_login.html', {'form': form})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def logout_view(request):
    logout(request)
    request.session.flush()
    messages.info(request, "You have been logged out.")
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def dashboard_view(request):
    members_count = FamilyMember.objects.filter(user=request.user).count()
    records_count = MedicalRecord.objects.filter(user=request.user).count()
    medicines_count = Medication.objects.filter(user=request.user).count()
    appointments_count = Appointment.objects.filter(user=request.user, status='Scheduled').count()

    recent_appointments = Appointment.objects.filter(user=request.user).select_related('member').order_by('-date')[:3]
    recent_records = MedicalRecord.objects.filter(user=request.user).select_related('member').order_by('-date_uploaded')[:3]

    context = {
        'members_count': members_count,
        'records_count': records_count,
        'medicines_count': medicines_count,
        'appointments_count': appointments_count,
        'recent_appointments': recent_appointments,
        'recent_records': recent_records,
    }
    return render(request, 'dashboard.html', context)

@admin_required
def admin_dashboard_view(request):
    search_query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', 'all')
    status_filter = request.GET.get('status', 'all')

    users_qs = User.objects.annotate(
        members_cnt=Count('family_members', distinct=True),
        records_cnt=Count('medical_records', distinct=True),
        medicines_cnt=Count('medications', distinct=True),
        appointments_cnt=Count('appointments', distinct=True),
    ).order_by('-date_joined')

    # Aggregated system metrics
    total_users_count = User.objects.count()
    admin_users_count = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    regular_users_count = total_users_count - admin_users_count
    total_members_count = FamilyMember.objects.count()
    total_records_count = MedicalRecord.objects.count()
    total_medicines_count = Medication.objects.count()
    total_appointments_count = Appointment.objects.count()

    # Search filters
    if search_query:
        users_qs = users_qs.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    # Role filter
    if role_filter == 'admin':
        users_qs = users_qs.filter(Q(is_staff=True) | Q(is_superuser=True))
    elif role_filter == 'user':
        users_qs = users_qs.filter(is_staff=False, is_superuser=False)

    # Status filter
    if status_filter == 'active':
        users_qs = users_qs.filter(is_active=True)
    elif status_filter == 'inactive':
        users_qs = users_qs.filter(is_active=False)

    context = {
        'users': users_qs,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'total_users_count': total_users_count,
        'admin_users_count': admin_users_count,
        'regular_users_count': regular_users_count,
        'total_members_count': total_members_count,
        'total_records_count': total_records_count,
        'total_medicines_count': total_medicines_count,
        'total_appointments_count': total_appointments_count,
    }
    return render(request, 'admin_dashboard.html', context)

@admin_required
def admin_user_detail_view(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    members = FamilyMember.objects.filter(user=target_user)
    records = MedicalRecord.objects.filter(user=target_user).select_related('member').order_by('-date_uploaded')
    medicines = Medication.objects.filter(user=target_user).select_related('member')
    appointments = Appointment.objects.filter(user=target_user).select_related('member').order_by('-date')

    context = {
        'target_user': target_user,
        'members': members,
        'records': records,
        'medicines': medicines,
        'appointments': appointments,
    }
    return render(request, 'admin_user_detail.html', context)

@admin_required
def admin_toggle_staff_view(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, pk=user_id)
        if target_user == request.user:
            messages.error(request, "You cannot alter your own admin status.")
        else:
            target_user.is_staff = not target_user.is_staff
            target_user.save()
            st = "granted Administrator status" if target_user.is_staff else "revoked Administrator status"
            messages.success(request, f"Successfully {st} for '{target_user.username}'.")
    return redirect('admin_dashboard')

@admin_required
def admin_toggle_active_view(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, pk=user_id)
        if target_user == request.user:
            messages.error(request, "You cannot deactivate your own admin account.")
        else:
            target_user.is_active = not target_user.is_active
            target_user.save()
            st = "activated" if target_user.is_active else "deactivated"
            messages.success(request, f"Successfully {st} account for '{target_user.username}'.")
    return redirect('admin_dashboard')

@admin_required
def admin_reset_password_view(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, pk=user_id)
        new_password = request.POST.get('new_password', '').strip()
        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        else:
            target_user.set_password(new_password)
            target_user.save()
            messages.success(request, f"Password reset successfully for '{target_user.username}'.")
    return redirect('admin_dashboard')

@admin_required
def admin_create_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '').strip()
        is_admin = request.POST.get('is_admin') == 'on'

        if not username or not password or not email:
            messages.error(request, "Username, Email, and Password are required.")
            return redirect('admin_dashboard')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken.")
            return redirect('admin_dashboard')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        if is_admin:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, f"Admin account '{username}' created successfully!")
        else:
            messages.success(request, f"User account '{username}' created successfully!")

    return redirect('admin_dashboard')

@admin_required
def admin_delete_user_view(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, pk=user_id)
        if target_user == request.user:
            messages.error(request, "You cannot delete your own logged-in admin account.")
        else:
            uname = target_user.username
            target_user.delete()
            messages.success(request, f"User '{uname}' and all associated records deleted.")
    return redirect('admin_dashboard')

