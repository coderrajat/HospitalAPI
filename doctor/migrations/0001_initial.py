# Generated by Django 4.1.5 on 2023-01-13 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctordetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docter_start_time', models.DateTimeField(auto_now=True, verbose_name='start_appointment')),
                ('docter_close_time', models.DateTimeField(auto_now=True, verbose_name='start_appointment')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=60, verbose_name='email')),
                ('country_code', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('country', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=100)),
                ('zip_code', models.CharField(default='', max_length=100)),
                ('address_line_1', models.CharField(default='', max_length=200)),
                ('address_line_2', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorAppoinment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(default='', max_length=100)),
                ('patient_problem', models.TextField(default='')),
                ('start_appointment', models.DateTimeField(auto_now=True, verbose_name='start_appointment')),
                ('end_appointment', models.DateTimeField(auto_now=True, verbose_name='start_appointment')),
                ('repeated_patient', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=60, verbose_name='email')),
                ('country_code', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('country', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=100)),
                ('zip_code', models.CharField(default='', max_length=100)),
                ('address_line_1', models.CharField(default='', max_length=200)),
                ('address_line_2', models.CharField(default='', max_length=200)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointment', to='doctor.doctordetails')),
            ],
        ),
    ]
