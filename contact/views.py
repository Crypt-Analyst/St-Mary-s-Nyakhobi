from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactInquiry
from .forms import ContactForm

def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact/contact.html', context)