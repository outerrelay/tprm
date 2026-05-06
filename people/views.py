from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from core.mixins import AuditMixin
from vendors.models import Vendor

from .forms import PersonForm, VendorPersonRelationshipForm
from .models import Person, VendorPersonRelationship


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    template_name = 'people/person_list.html'
    context_object_name = 'people'

    def get_queryset(self):
        qs = Person.objects.annotate(
            vendor_count=Count('vendor_links', distinct=True),
        )
        q = self.request.GET.get('q', '').strip()
        role = self.request.GET.get('role', '').strip()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                | Q(middle_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
                | Q(phone__icontains=q)
                | Q(vendor_links__vendor__name__icontains=q)
                | Q(vendor_links__relationship_type__icontains=q)
            ).distinct()
        if role:
            qs = qs.filter(vendor_links__relationship_type=role).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['current_role'] = self.request.GET.get('role', '')
        ctx['role_choices'] = VendorPersonRelationship.RelationshipType.choices
        return ctx


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'people/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['vendor_links'] = (
            self.object.vendor_links.select_related('vendor').all()
        )
        return ctx


class PersonCreateView(LoginRequiredMixin, AuditMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'people/person_form.html'

    def get_success_url(self):
        vendor_pk = self.request.GET.get('vendor')
        if vendor_pk:
            return (
                reverse('people:relationship_create', kwargs={'vendor_pk': vendor_pk})
                + f'?person={self.object.pk}'
            )
        return reverse('people:person_detail', kwargs={'pk': self.object.pk})


class PersonUpdateView(LoginRequiredMixin, AuditMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'people/person_form.html'

    def get_success_url(self):
        return reverse('people:person_detail', kwargs={'pk': self.object.pk})


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    model = Person
    template_name = 'people/person_confirm_delete.html'
    success_url = reverse_lazy('people:person_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['link_count'] = self.object.vendor_links.count()
        return ctx


class VendorPersonRelationshipCreateView(LoginRequiredMixin, AuditMixin, CreateView):
    model = VendorPersonRelationship
    form_class = VendorPersonRelationshipForm
    template_name = 'people/relationship_form.html'

    def get_initial(self):
        initial = super().get_initial()
        person_pk = self.request.GET.get('person')
        if person_pk:
            initial['person'] = person_pk
        return initial

    def form_valid(self, form):
        form.instance.vendor_id = self.kwargs['vendor_pk']
        response = super().form_valid(form)
        rt = form.cleaned_data.get('relationship_type')
        ownership = form.cleaned_data.get('ownership_percentage')
        if rt in ('shareholder', 'beneficial_owner') and ownership is None:
            messages.warning(
                self.request,
                'Ownership percentage is recommended for shareholders and beneficial owners.',
            )
        return response

    def get_success_url(self):
        return reverse('vendors:vendor_detail', kwargs={'pk': self.kwargs['vendor_pk']})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['vendor'] = get_object_or_404(Vendor, pk=self.kwargs['vendor_pk'])
        return ctx


class VendorPersonRelationshipUpdateView(LoginRequiredMixin, AuditMixin, UpdateView):
    model = VendorPersonRelationship
    form_class = VendorPersonRelationshipForm
    template_name = 'people/relationship_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        rt = form.cleaned_data.get('relationship_type')
        ownership = form.cleaned_data.get('ownership_percentage')
        if rt in ('shareholder', 'beneficial_owner') and ownership is None:
            messages.warning(
                self.request,
                'Ownership percentage is recommended for shareholders and beneficial owners.',
            )
        return response

    def get_success_url(self):
        return reverse('vendors:vendor_detail', kwargs={'pk': self.object.vendor_id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['vendor'] = self.object.vendor
        return ctx


class VendorPersonRelationshipDeleteView(LoginRequiredMixin, DeleteView):
    model = VendorPersonRelationship
    template_name = 'people/relationship_confirm_delete.html'

    def get_success_url(self):
        return reverse('vendors:vendor_detail', kwargs={'pk': self.object.vendor_id})
