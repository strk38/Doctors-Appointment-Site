# Generated by Django 5.0 on 2023-12-13 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_alter_appointment_accepted_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='lasst_name',
            new_name='last_name',
        ),
    ]
