from django import forms
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import ContactInquiry

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'inquiry_type', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6'),
                Column('inquiry_type', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'subject',
            'message',
            Submit('submit', 'Send Message', css_class='btn btn-primary')
        )
        
        # Add CSS classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add placeholders
        self.fields['name'].widget.attrs.update({'placeholder': 'Your Full Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'your.email@example.com'})
        self.fields['phone'].widget.attrs.update({'placeholder': '(555) 123-4567'})
        self.fields['subject'].widget.attrs.update({'placeholder': 'Brief subject of your inquiry'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Please provide details about your inquiry...'})
    
    def send_email(self):
        """Send email notification after form submission"""
        try:
            # Prepare email content
            subject = f"New Contact Form Submission: {self.cleaned_data['subject']}"
            
            message = f"""
New contact form submission from St. Mary's Nyakhobi website:

Name: {self.cleaned_data['name']}
Email: {self.cleaned_data['email']}
Phone: {self.cleaned_data.get('phone', 'Not provided')}
Inquiry Type: {self.cleaned_data.get('inquiry_type', 'General')}
Subject: {self.cleaned_data['subject']}

Message:
{self.cleaned_data['message']}

---
This message was sent from the St. Mary's Nyakhobi Senior School website contact form.
"""
            
            # Send email to school administrators
            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@stmarysnyakhobi.ac.ke'),
                recipient_list=[
                    getattr(settings, 'CONTACT_EMAIL', 'info@stmarysnyakhobi.ac.ke'),
                    getattr(settings, 'PRINCIPAL_EMAIL', 'principal@stmarysnyakhobi.ac.ke'),
                ],
                fail_silently=False,
            )
            
            # Send confirmation email to sender
            confirmation_subject = "Thank you for contacting St. Mary's Nyakhobi Senior School"
            confirmation_message = f"""
Dear {self.cleaned_data['name']},

Thank you for contacting St. Mary's Nyakhobi Senior School. We have received your inquiry regarding "{self.cleaned_data['subject']}" and will respond within 24-48 hours.

Your message:
{self.cleaned_data['message']}

If you need immediate assistance, please call us at +254 712 345 678.

Best regards,
St. Mary's Nyakhobi Senior School
Administration Office
"""
            
            send_mail(
                subject=confirmation_subject,
                message=confirmation_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@stmarysnyakhobi.ac.ke'),
                recipient_list=[self.cleaned_data['email']],
                fail_silently=True,  # Don't fail if confirmation email fails
            )
            
            return True
            
        except Exception as e:
            # Log the error (in production, use proper logging)
            print(f"Email sending failed: {str(e)}")
            return False
        self.fields['subject'].widget.attrs.update({'placeholder': 'Brief subject of your inquiry'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Please describe your inquiry in detail...'})