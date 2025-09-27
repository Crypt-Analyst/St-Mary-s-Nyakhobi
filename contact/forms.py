from django import forms
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
        self.fields['message'].widget.attrs.update({'placeholder': 'Please describe your inquiry in detail...'})