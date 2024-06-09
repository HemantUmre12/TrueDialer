from rest_framework import serializers

from .models import CustomUser, SpamReport


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "phone_number", "email"]

    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception=raise_exception)

        if valid:
            phone_number = self.validated_data["phone_number"]
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                self.errors["phone"] = ["phone number already exists"]
                valid = False

        return valid

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)

        return user


class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ["id", "phone_number"]

    def create(self, validated_data):
        user = self.context["request"].user

        spamReport = SpamReport.objects.create(reported_by=user, **validated_data)

        return spamReport
