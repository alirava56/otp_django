# برای  ارسال otp 

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import OTP


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        email = value.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "کاربری با این ایمیل قبلاً ثبت‌نام کرده است."
            )

        return email


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    full_name = serializers.CharField(
        max_length=150
    )

    password = serializers.CharField(
        write_only=True
    )

    otp = serializers.CharField(
        min_length=6,
        max_length=6,
        write_only=True
    )

    def validate_email(self, value):
        email = value.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "کاربری با این ایمیل قبلاً ثبت‌نام کرده است."
            )

        return email

    def validate_password(self, value):
        validate_password(value)

        return value

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "کد OTP باید فقط شامل عدد باشد."
            )

        return value

    def validate(self, attrs):
        email = attrs["email"]
        otp_code = attrs["otp"]

        otp = (
            OTP.objects
            .filter(
                email=email,
                is_used=False
            )
            .order_by("-created_at")
            .first()
        )

        if otp is None:
            raise serializers.ValidationError({
                "otp": "کد OTP برای این ایمیل پیدا نشد."
            })

        if otp.is_expired():
            raise serializers.ValidationError({
                "otp": "کد OTP منقضی شده است. کد جدید دریافت کنید."
            })

        if otp.code != otp_code:
            raise serializers.ValidationError({
                "otp": "کد OTP صحیح نیست."
            })

        attrs["otp_object"] = otp

        return attrs

    def create(self, validated_data):
        otp = validated_data.pop("otp_object")

        validated_data.pop("otp")

        email = validated_data["email"]
        full_name = validated_data["full_name"]
        password = validated_data["password"]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        return user