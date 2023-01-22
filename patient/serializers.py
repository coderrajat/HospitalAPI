from rest_framework import serializers



class booking_fields(serializers.Serializer):
    phone_number=serializers.IntegerField()
    patient_problem=serializers.CharField()
    start_appointment=serializers.DateTimeField()
    end_appointment=serializers.DateTimeField()
    repeated_patient=serializers.BooleanField(default=False)
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    date_of_birth=serializers.CharField()
    gender=serializers.CharField()
    email=serializers.EmailField()
    country_code=serializers.CharField()
    phone_number=serializers.CharField()
    country=serializers.CharField()
    city=serializers.CharField()
    state=serializers.CharField()
    zip_code=serializers.CharField()
    address_line_1=serializers.CharField()
    address_line_2=serializers.CharField()