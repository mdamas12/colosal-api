from rest_framework import serializers
from django import forms
from .models import *




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoriesDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'image'
        )
