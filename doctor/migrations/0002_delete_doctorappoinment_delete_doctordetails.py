# Generated by Django 4.0 on 2023-01-22 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DoctorAppoinment',
        ),
        migrations.DeleteModel(
            name='Doctordetails',
        ),
    ]