from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdmissionApplication, AdmissionRequirement
from .forms import AdmissionApplicationForm

def admission_info(request):
    """General admission information"""
    context = {}
    return render(request, 'admissions/info.html', context)

def apply(request):
    """Admission application form"""
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('admissions:apply')
    else:
        form = AdmissionApplicationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'admissions/apply.html', context)

def requirements(request):
    """Admission requirements by grade level"""
    requirements = AdmissionRequirement.objects.all().order_by('grade_level')
    
    context = {
        'requirements': requirements,
    }
    return render(request, 'admissions/requirements.html', context)