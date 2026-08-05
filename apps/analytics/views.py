from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.members.models import FamilyMember
from .models import HealthMetric
from .forms import HealthMetricForm

@login_required
def health_analytics_view(request):
    user_members = FamilyMember.objects.filter(user=request.user)
    if request.method == 'POST':
        form = HealthMetricForm(request.POST)
        form.fields['member'].queryset = user_members
        if form.is_valid():
            metric = form.save(commit=False)
            metric.user = request.user
            metric.save()
            messages.success(request, "Health vitals recorded.")
            return redirect('health_analytics')
        else:
            messages.error(request, "Error saving health vitals. Please check form inputs.")
    else:
        form = HealthMetricForm()
        form.fields['member'].queryset = user_members
    
    metrics = HealthMetric.objects.filter(user=request.user).select_related('member').order_by('-record_date')
    return render(request, 'health_analytics.html', {'metrics': metrics, 'form': form})

@login_required
def delete_health_metric(request, pk):
    metric = get_object_or_404(HealthMetric, pk=pk, user=request.user)
    metric.delete()
    messages.success(request, "Health vitals entry removed.")
    return redirect('health_analytics')
