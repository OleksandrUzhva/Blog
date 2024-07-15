from django.contrib.auth.hashers import make_password
from rest_framework import serializers, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.cache import CacheService

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
        ]  

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        return attrs


class UserRegistrationPublickSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class ActivationSerializer(serializers.Serializer):
    key = serializers.UUIDField()


class UserAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(is_active=True) 

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            UserRegistrationPublickSerializer(serializer.data).data,
            status=status.HTTP_201_CREATED)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = UserRegistrationPublickSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"
    permission_classes = [permissions.AllowAny]
    

class UserActivationAPI(APIView):
    serializer_class = ActivationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        key = serializer.validated_data.get("key")
        cache = CacheService()
        activation_info = cache.get(namespace="activation", key=key)
        user_id = activation_info.get("user_id")
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return Response(
            {"Your email is successfully activated"}, status=status.HTTP_200_OK  # noqa
        )