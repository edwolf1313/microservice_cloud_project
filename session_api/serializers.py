from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from session_api.models import (
    AuthToken,
    session_client_data,
)

class SessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = session_client_data
        fields = "__all__"

    def create(self, validated_data):
        validated_data['client_secret'] = make_password(validated_data.get('client_secret'))
        application = session_client_data(**validated_data)
        application.save()
        return application


class AuthTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = "__all__"

    def create(self, validated_data):
        authtoken = AuthToken(**validated_data)
        authtoken.save()
        return authtoken
