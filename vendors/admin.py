from django.contrib import admin
from .models import Vendor, Assessment


class AssessmentInline(admin.TabularInline):
    model = Assessment
    extra = 0
    show_change_link = True
    fields = ['title', 'category', 'status', 'inherent_rating', 'residual_rating']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'status', 'contact_email', 'created_at']
    list_filter = ['tier', 'status']
    search_fields = ['name', 'contact_name', 'contact_email']
    inlines = [AssessmentInline]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'title', 'category', 'status', 'inherent_rating', 'residual_rating', 'created_at']
    list_filter = ['status', 'category', 'inherent_rating']
    search_fields = ['vendor__name', 'title']
