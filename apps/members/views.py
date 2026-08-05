from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FamilyMember
from .forms import FamilyMemberForm

@login_required
def family_members_view(request):
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, f"Family member '{member.name}' added successfully!")
            return redirect('family_members')
        else:
            messages.error(request, "Error adding family member. Please check form inputs.")
    else:
        form = FamilyMemberForm()
    
    members = FamilyMember.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'family_members.html', {'members': members, 'form': form})

@login_required
def delete_family_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, user=request.user)
    member.delete()
    messages.success(request, "Family member removed.")
    return redirect('family_members')
