from rest_framework import serializers
from .models import Category, Product,Brand, UserAddressBook,ProductAttribute

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields ='__all__'

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand
		fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model =  UserAddressBook
		fields =  '__all__'

class ProductAttributeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductAttribute
		fields = '__all__'
		#fields = ['color']

