from django.contrib import admin

from people.admin import VendorPersonRelationshipInline

from .models import Assessment, Vendor


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
    readonly_fields = ['vendor_id', 'created_at', 'updated_at', 'created_by', 'updated_by']
    inlines = [AssessmentInline, VendorPersonRelationshipInline]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'title', 'category', 'status', 'inherent_rating', 'residual_rating', 'created_at']
    list_filter = ['status', 'category', 'inherent_rating']
    search_fields = ['vendor__name', 'title']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
