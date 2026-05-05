from django import forms
from .models import Vendor, Assessment


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'description', 'tier', 'status', 'website', 'contact_name', 'contact_email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tier': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = [
            'title', 'category', 'status',
            'inherent_rating', 'residual_rating',
            'notes', 'started_at', 'completed_at',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'inherent_rating': forms.Select(attrs={'class': 'form-select'}),
            'residual_rating': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'started_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
