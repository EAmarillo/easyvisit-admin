# Generated by Django 4.2.6 on 2023-10-30 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urbanizations', '0001_initial'),
        ('urbanization_managers', '0005_alter_urbanizationmanager_urbanization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urbanizationmanager',
            name='urbanization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urbanizationmanager', to='urbanizations.urbanization'),
        ),
    ]
