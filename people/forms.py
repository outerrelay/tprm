from django import forms

from core.forms import BootstrapFormMixin

from .models import Person, VendorPersonRelationship


class PersonForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'middle_name', 'last_name',
            'email', 'phone',
            'country_of_residence', 'nationality', 'date_of_birth',
            'notes',
        ]
        widgets = {
            'nationality': forms.TextInput(attrs={'placeholder': 'e.g. Canadian, French'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class VendorPersonRelationshipForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = VendorPersonRelationship
        fields = [
            'person', 'relationship_type', 'title',
            'ownership_percentage', 'is_primary_contact', 'is_active',
            'start_date', 'end_date', 'notes',
        ]
        widgets = {
            'ownership_percentage': forms.NumberInput(attrs={
                'step': '0.01', 'min': '0', 'max': '100',
            }),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', 'End date must be on or after start date.')
        return cleaned
