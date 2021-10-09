
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, login
from rest_framework import serializers

from rest_framework.authtoken.models import Token

from api.models import Category

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):

    token = serializers.CharField(required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserSignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField(required=True, allow_null=False, allow_blank=False,
                                                      validators=[UniqueValidator(queryset=User.objects.all())])
        self.fields['first_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['last_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'token')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        return user validate data
        """
        request = self._kwargs['context']['request']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        category_list = ['Fuel', 'Bill', 'Entertainment', 'Education', 'Food']
        for category in category_list:
            user.user_categories.create(name=category)
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        validated_data["token"] = token.key
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):

    token = serializers.CharField(required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.fields['password'] = serializers.CharField(required=True, allow_null=False, allow_blank=False,)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')


class NewCategorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Category
        fields = ('user', 'name',)
        extra_kwargs = {'name': {'required': True}, 'read_only': {'read_only': True}}

    def create(self, validated_data):
        """
        return category object.
        """
        request = self._kwargs['context']['request']
        user = request.user
        validated_data['user'] = user
        name = validated_data["name"]
        user.user_categories.get_or_create(name=name)
        validated_data['message'] = 'New Category Created!'
        return validated_data







