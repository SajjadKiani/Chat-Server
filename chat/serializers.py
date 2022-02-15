from .models import User
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(first_name=validated_data['first_name']
                                       ,last_name=validated_data['last_name']
                                       , username=validated_data['username']
                                       , email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
