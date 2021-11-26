from rest_framework import serializers

from main.models import AdvUser, Categories, Operations

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdvUser
        fields =[
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        ]