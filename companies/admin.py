from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'name', 'country_of_incorporation', 'updated_at']
    search_fields = ['company_id', 'name', 'registration_number']
    readonly_fields = ['company_id', 'created_at', 'updated_at', 'created_by', 'updated_by']
    ordering = ['name']
