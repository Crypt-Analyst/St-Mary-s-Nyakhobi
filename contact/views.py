from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactInquiry
from .forms import ContactForm

def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to database
            contact_inquiry = form.save()
            
            # Send email notifications
            email_sent = form.send_email()
            
            if email_sent:
                messages.success(
                    request, 
                    'Thank you for your message! We have received your inquiry and will respond within 24-48 hours. A confirmation email has been sent to your email address.'
                )
            else:
                messages.success(
                    request, 
                    'Thank you for your message! We have received your inquiry and will get back to you soon.'
                )
                messages.warning(
                    request,
                    'Note: There was an issue sending the confirmation email, but your message has been saved.'
                )
            
            return redirect('contact:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact/info.html', context)