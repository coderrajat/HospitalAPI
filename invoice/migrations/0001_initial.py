# Generated by Django 4.1.5 on 2023-01-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patientbills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_problem', models.TextField(default='')),
                ('hospital_name', models.CharField(default='', max_length=100)),
                ('patient_first_name', models.CharField(max_length=100)),
                ('Patient_last_name', models.CharField(max_length=100)),
                ('services_taken', models.CharField(max_length=100)),
                ('total_time', models.TextField(default='')),
                ('amount', models.CharField(default='0', max_length=100)),
                ('service_charge', models.CharField(default='0', max_length=100)),
                ('additional_charges', models.CharField(default='0', max_length=100)),
                ('discount', models.CharField(default='0', max_length=100)),
                ('tax', models.CharField(default='0', max_length=100)),
                ('total', models.CharField(default='0', max_length=100)),
                ('invoice_id', models.TextField(unique=True)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
