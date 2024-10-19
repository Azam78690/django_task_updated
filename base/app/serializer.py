from rest_framework import serializers
from .models import Client_model,Project_model
from django.contrib.auth.models import User

class client_serializer(serializers.ModelSerializer):
        class Meta:
                model = Client_model
                fields = '__all__'
                read_only_fields = ['created_by']


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class project_serializer(serializers.ModelSerializer):

    class Meta:
        model = Project_model
        fields = '__all__'



