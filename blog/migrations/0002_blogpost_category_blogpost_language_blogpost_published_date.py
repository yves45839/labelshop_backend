from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='language',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-published_date', '-created_at']},
        ),
    ]
