# Generated by Django 4.2.6 on 2023-10-30 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urbanizations', '0003_remove_urbanizations_houses_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='urbanizations',
            old_name='plan_id',
            new_name='plan',
        ),
    ]