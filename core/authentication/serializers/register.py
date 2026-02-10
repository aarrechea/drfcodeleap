from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'error_messages': {
                    'unique': 'A user with this email already exists.'
                }
            },
            'username': {
                'error_messages': {
                    'unique': 'A user with this username already exists.'
                }
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

