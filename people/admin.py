from django.contrib import admin

from .models import Person, VendorPersonRelationship


class VendorPersonRelationshipInline(admin.TabularInline):
    model = VendorPersonRelationship
    extra = 0
    show_change_link = True
    fields = [
        'vendor', 'person', 'relationship_type', 'title',
        'ownership_percentage', 'is_primary_contact', 'is_active',
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'person_id', 'last_name', 'first_name', 'email', 'phone',
        'country_of_residence', 'updated_at',
    ]
    list_filter = ['country_of_residence']
    search_fields = [
        'person_id', 'first_name', 'middle_name', 'last_name',
        'email', 'phone', 'nationality',
    ]
    readonly_fields = ['person_id', 'created_at', 'updated_at', 'created_by', 'updated_by']
    inlines = [VendorPersonRelationshipInline]


@admin.register(VendorPersonRelationship)
class VendorPersonRelationshipAdmin(admin.ModelAdmin):
    list_display = [
        'vendor', 'person', 'relationship_type', 'title',
        'ownership_percentage', 'is_primary_contact', 'is_active',
        'start_date', 'end_date',
    ]
    list_filter = ['relationship_type', 'is_active', 'is_primary_contact']
    search_fields = [
        'vendor__company__name', 'person__first_name', 'person__last_name',
        'person__email', 'title',
    ]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
