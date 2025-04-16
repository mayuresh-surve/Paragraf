from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=CustomUser.objects.all(), message="User with this email already exists.")])
    password = serializers.CharField(write_only=True, required=True, min_length=8, error_messages={
                                     "min_length": "Password must be at least 8 characters long."})
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", "password",
                  "date_joined", "first_name", "last_name", "gender", "dob", "profile_pic_url", "bio")

    def create(self, validated_data):
        try:
            # Create user in the users table
            user = CustomUser.objects.create_user(**validated_data)
        except ValueError as e:
            # This will return a 400 response with the error message
            raise serializers.ValidationError({"detail": str(e)})
        return user
