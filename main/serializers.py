from rest_framework import serializers

from main.models import AdvUser, Category, Operation


class UsersSerializer(serializers.ModelSerializer):
    # class UsersSerializer(serializers.HyperlinkedModelSerializer):
    # operations = OperationsSerializer(many=True)

    class Meta:
        model = AdvUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            # 'operations',
        ]


class CategoriesSerializer(serializers.ModelSerializer):
    # class UsersSerializer(serializers.HyperlinkedModelSerializer):
    # operations = OperationsSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'cat_type',
        ]


class OperationsSerializer(serializers.ModelSerializer):
    # user = UsersSerializer()
    # category = CategoriesSerializer()

    class Meta:
        model = Operation
        fields = [
            'id',
            'title',
            'description',
            'amount',
            'user',
            'category',
            'created_at',
        ]
