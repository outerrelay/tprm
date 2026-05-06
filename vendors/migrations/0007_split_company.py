"""Split Vendor.name/description/website out into a separate Company model.

Step-by-step so existing vendor data survives the migration:

    1. Add nullable `vendor.company` FK to Company.
    2. RunPython: for each existing Vendor, create a Company with the
       current name/description/website and link it.
    3. Make `vendor.company` non-nullable.
    4. Remove the now-orphaned name/description/website fields from Vendor.

Reverse migration is supported — restores Vendor.name/description/website
from the linked Company record before dropping the FK.
"""

import django.db.models.deletion
from django.db import migrations, models


def _next_company_id(apps):
    Company = apps.get_model('companies', 'Company')
    last = Company.objects.order_by('id').last()
    return (last.pk if last else 0) + 1


def populate_companies(apps, schema_editor):
    Vendor = apps.get_model('vendors', 'Vendor')
    Company = apps.get_model('companies', 'Company')

    next_pk = _next_company_id(apps)
    for vendor in Vendor.objects.all():
        company = Company.objects.create(
            name=vendor.name,
            description=vendor.description or '',
            website=vendor.website or '',
            company_id=f'CMP-{next_pk:04d}',
        )
        next_pk += 1
        vendor.company = company
        vendor.save(update_fields=['company'])


def restore_vendor_fields(apps, schema_editor):
    Vendor = apps.get_model('vendors', 'Vendor')
    for vendor in Vendor.objects.select_related('company').all():
        if vendor.company is None:
            continue
        vendor.name = vendor.company.name
        vendor.description = vendor.company.description
        vendor.website = vendor.company.website
        vendor.save(update_fields=['name', 'description', 'website'])


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('vendors', '0006_assessment_created_by_assessment_updated_by_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['company__name']},
        ),
        migrations.AddField(
            model_name='vendor',
            name='company',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='vendor_profile',
                to='companies.company',
            ),
        ),
        migrations.RunPython(populate_companies, restore_vendor_fields),
        migrations.AlterField(
            model_name='vendor',
            name='company',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='vendor_profile',
                to='companies.company',
            ),
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='description',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='website',
        ),
    ]
