from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserDocument, Team, StaffDocument
from django.contrib.auth.models import User


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "user", "team_members", "team", "description")
        extra_kwargs = {"user": {"write_only": True}}


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class UserDocumentUploadSerializer(ModelSerializer):
    document = serializers.FileField(use_url=True)
    expiry_date = serializers.DateField()

    class Meta:
        model = UserDocument
        fields = [
            "qualification_categories",
            "uploader",
            "document",
            "expiry_date",
        ]
        read_only_fields = ["uploader"]


class StaffDocumentUploadSerializer(ModelSerializer):
    document = serializers.FileField(use_url=True)
    expiry_date = serializers.DateField()

    class Meta:
        model = StaffDocument
        fields = [
            "uploader",
            "document",
            "client_categories",
            "expiry_date",
        ]
