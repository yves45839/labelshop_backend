from django.db import migrations


def create_sites(apps, schema_editor):
    Site = apps.get_model('inventory', 'Site')
    for name in ['Abobo', 'Treichville', 'Riviera 2']:
        Site.objects.get_or_create(name=name)

def delete_sites(apps, schema_editor):
    Site = apps.get_model('inventory', 'Site')
    Site.objects.filter(name__in=['Abobo', 'Treichville', 'Riviera 2']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sites, delete_sites),
    ]
