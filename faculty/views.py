from django.shortcuts import render
from .models import Faculty, Department

def faculty_list(request):
    """Display all faculty members"""
    departments = Department.objects.all()
    faculty_members = Faculty.objects.filter(is_active=True)
    
    # Group faculty by position for leadership (principal and vice principals)
    leadership = faculty_members.filter(position__in=['principal', 'vice_principal'])
    teachers = faculty_members.filter(position='teacher')
    admin_staff = faculty_members.filter(position='admin_staff')
    support_staff = faculty_members.filter(position='support_staff')
    
    context = {
        'departments': departments,
        'leadership': leadership,
        'teachers': teachers,
        'admin_staff': admin_staff,
        'support_staff': support_staff,
    }
    return render(request, 'faculty/staff.html', context)

def department_detail(request, department_id):
    """Display faculty by department"""
    department = Department.objects.get(id=department_id)
    faculty_members = Faculty.objects.filter(department=department, is_active=True)
    
    context = {
        'department': department,
        'faculty_members': faculty_members,
    }
    return render(request, 'faculty/department_detail.html', context)