from django.shortcuts import render, get_object_or_404
from .models import AcademicProgram, GradeLevel, Subject, AcademicCalendar

def programs(request):
    """Display all academic programs"""
    programs = AcademicProgram.objects.all()
    grade_levels = GradeLevel.objects.all()
    
    context = {
        'programs': programs,
        'grade_levels': grade_levels,
    }
    return render(request, 'academics/programs.html', context)

def program_detail(request, program_id):
    """Display detailed information about a specific program"""
    program = get_object_or_404(AcademicProgram, id=program_id)
    
    context = {
        'program': program,
    }
    return render(request, 'academics/program_detail.html', context)

def academic_calendar(request):
    """Display academic calendar"""
    calendar_events = AcademicCalendar.objects.all().order_by('start_date')
    
    context = {
        'calendar_events': calendar_events,
    }
    return render(request, 'academics/calendar.html', context)