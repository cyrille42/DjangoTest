from django.contrib.auth.models import User, Group
from rest_framework import serializers
from stock.models import Product, Cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        discount = data['discount']
        if not (0 <= discount <= 100):
            raise serializers.ValidationError('A discount must be between 0 and 100')

        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'validation']

    def create(self, validated_data):
        validated_data['username'] = self.context['request'].user
        return super(CartSerializer, self).create(validated_data)
