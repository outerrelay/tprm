from django import forms

from .models import Person, VendorPersonRelationship


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'middle_name', 'last_name',
            'email', 'phone',
            'country_of_residence', 'nationality', 'date_of_birth',
            'notes',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'country_of_residence': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Canadian, French',
            }),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class VendorPersonRelationshipForm(forms.ModelForm):
    class Meta:
        model = VendorPersonRelationship
        fields = [
            'person', 'relationship_type', 'title',
            'ownership_percentage', 'is_primary_contact', 'is_active',
            'start_date', 'end_date', 'notes',
        ]
        widgets = {
            'person': forms.Select(attrs={'class': 'form-select'}),
            'relationship_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'ownership_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01', 'min': '0', 'max': '100',
            }),
            'is_primary_contact': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', 'End date must be on or after start date.')
        return cleaned
