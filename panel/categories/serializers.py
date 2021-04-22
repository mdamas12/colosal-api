from rest_framework import serializers
from django import forms
from .models import *




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'image'
        )

class CategoriesDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'image'
        )
