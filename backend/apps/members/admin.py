from django.contrib import admin
from .models import FamilyMember

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'relation', 'age', 'gender', 'blood_group', 'user')
    search_fields = ('name', 'relation')
    list_filter = ('gender', 'blood_group')
