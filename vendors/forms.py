from django import forms

from companies.models import Company
from core.forms import BootstrapFormMixin

from .models import Assessment, Vendor


class VendorForm(BootstrapFormMixin, forms.ModelForm):
    """Edits a Vendor and its underlying Company in one form.

    The user-visible fields `name`, `description`, `website` belong to Company;
    `tier`, `status`, `contact_name`, `contact_email` belong to Vendor. The form
    creates or updates both records on save.
    """

    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    website = forms.URLField(required=False)

    field_order = [
        'name', 'description', 'tier', 'status', 'website',
        'contact_name', 'contact_email',
    ]

    class Meta:
        model = Vendor
        fields = ['tier', 'status', 'contact_name', 'contact_email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            company = self.instance.company
            self.fields['name'].initial = company.name
            self.fields['description'].initial = company.description
            self.fields['website'].initial = company.website

    def save(self, commit=True):
        if self.instance.pk:
            company = self.instance.company
        else:
            company = Company()
        company.name = self.cleaned_data['name']
        company.description = self.cleaned_data.get('description', '')
        company.website = self.cleaned_data.get('website', '')
        if commit:
            company.save()
        self.instance.company = company
        return super().save(commit=commit)


class AssessmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Assessment
        fields = [
            'title', 'category', 'status',
            'inherent_rating', 'residual_rating',
            'notes', 'started_at', 'completed_at',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'started_at': forms.DateInput(attrs={'type': 'date'}),
            'completed_at': forms.DateInput(attrs={'type': 'date'}),
        }
