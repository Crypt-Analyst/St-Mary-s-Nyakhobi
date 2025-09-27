from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from .models import AdmissionApplication

class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'student_first_name', 'student_last_name', 'date_of_birth', 'grade_level',
            'parent_first_name', 'parent_last_name', 'parent_email', 'parent_phone',
            'address', 'previous_school', 'medical_conditions', 'additional_notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Student Information',
                Row(
                    Column('student_first_name', css_class='form-group col-md-6'),
                    Column('student_last_name', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
                Row(
                    Column('date_of_birth', css_class='form-group col-md-6'),
                    Column('grade_level', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'Parent/Guardian Information',
                Row(
                    Column('parent_first_name', css_class='form-group col-md-6'),
                    Column('parent_last_name', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
                Row(
                    Column('parent_email', css_class='form-group col-md-6'),
                    Column('parent_phone', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
                'address',
            ),
            Fieldset(
                'Additional Information',
                'previous_school',
                'medical_conditions',
                'additional_notes',
            ),
            Submit('submit', 'Submit Application', css_class='btn btn-primary btn-lg')
        )
        
        # Add CSS classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add placeholders and help text
        self.fields['student_first_name'].widget.attrs.update({'placeholder': "Student's First Name"})
        self.fields['student_last_name'].widget.attrs.update({'placeholder': "Student's Last Name"})
        self.fields['parent_first_name'].widget.attrs.update({'placeholder': "Parent's First Name"})
        self.fields['parent_last_name'].widget.attrs.update({'placeholder': "Parent's Last Name"})
        self.fields['parent_email'].widget.attrs.update({'placeholder': 'parent@example.com'})
        self.fields['parent_phone'].widget.attrs.update({'placeholder': '(555) 123-4567'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Full home address including city, state, and zip code'})
        self.fields['previous_school'].widget.attrs.update({'placeholder': 'Name of previous school (if applicable)'})
        self.fields['medical_conditions'].widget.attrs.update({'placeholder': 'Any medical conditions, allergies, or special needs we should be aware of'})
        self.fields['additional_notes'].widget.attrs.update({'placeholder': 'Any additional information you would like to share'})