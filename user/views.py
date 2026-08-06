import secrets

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTP
from .serializers import (
    SendOTPSerializer,
    RegisterSerializer,
)


class SendOTPView(APIView):

    def post(self, request):
        serializer = SendOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]

        OTP.objects.filter(
            email=email,
            is_used=False
        ).delete()

        code = f"{secrets.randbelow(1000000):06d}"

        OTP.objects.create(
            email=email,
            code=code
        )

        return Response(
            {
                "message": "OTP با موفقیت ساخته شد.",
                "otp": code
            },
            status=status.HTTP_201_CREATED
        )


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "ثبت‌نام با موفقیت انجام شد.",
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.first_name,
                    "date_joined": user.date_joined
                }
            },
            status=status.HTTP_201_CREATED
        )