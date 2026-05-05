from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Vendor, Assessment
from .forms import VendorForm, AssessmentForm


class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'vendors/vendor_list.html'
    context_object_name = 'vendors'


class VendorDetailView(LoginRequiredMixin, DetailView):
    model = Vendor
    template_name = 'vendors/vendor_detail.html'
    context_object_name = 'vendor'


class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendors:vendor_list')


class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendors:vendor_list')


class AssessmentCreateView(LoginRequiredMixin, CreateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = 'vendors/assessment_form.html'

    def form_valid(self, form):
        form.instance.vendor_id = self.kwargs['vendor_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vendors:assessment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['vendor'] = Vendor.objects.get(pk=self.kwargs['vendor_pk'])
        return ctx


class AssessmentDetailView(LoginRequiredMixin, DetailView):
    model = Assessment
    template_name = 'vendors/assessment_detail.html'
    context_object_name = 'assessment'


class AssessmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = 'vendors/assessment_form.html'

    def get_success_url(self):
        return reverse_lazy('vendors:assessment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['vendor'] = self.object.vendor
        return ctx
