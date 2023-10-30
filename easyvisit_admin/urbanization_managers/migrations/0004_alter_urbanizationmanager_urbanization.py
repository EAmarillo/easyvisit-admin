# Generated by Django 4.2.6 on 2023-10-30 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urbanizations', '0001_initial'),
        ('urbanization_managers', '0003_alter_urbanizationmanager_urbanization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urbanizationmanager',
            name='urbanization',
            field=models.OneToOneField(db_column='urbanization_id', on_delete=django.db.models.deletion.CASCADE, to='urbanizations.urbanization'),
        ),
    ]
