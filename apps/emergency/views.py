from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.members.models import FamilyMember

@login_required
def emergency_view(request):
    members = FamilyMember.objects.filter(user=request.user)
    return render(request, 'emergency.html', {'members': members})
