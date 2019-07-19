from django.contrib import admin
from .models import StaffMember, Department


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'name', 
            'work_department',
            'phone_num',
            'grade',
            'school_department',
            'major',
            'personal_signature',
            'brief_introduction',
            'start_entry',
            'end_quit',
            'is_incumbent',
            'is_first_generation',
            'is_man',
            'is_delisting',
        )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brief_introduction', 'is_delete')
