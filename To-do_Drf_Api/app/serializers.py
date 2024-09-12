"""
Serializer for app.
"""

from app.models import *

from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class HelloSerializer(serializers.Serializer):
    """
    Testing serializer.
    """
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users.
    """
    class Meta:

        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password']
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        """
        return get_user_model().objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    conform_password = serializers.CharField(required=True) 


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tags.
    """
    class Meta:
        model = Tag
        fields = ['id','name']
        read_only_fields = ['id']


class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for Todo.
    """
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Todo
        fields = ['id','task', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self,tags,todo):
        """
        Handle getting or creating tags as needed.
        """
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            todo.tags.add(tag_obj)

    def create(self, validated_data):
        """
        Create a new todo object.
        """
        tags = validated_data.pop('tags', [])
        todo = Todo.objects.create(**validated_data)
        self._get_or_create_tags(tags,todo)
         
        return todo
    
    def update(self, instance, validated_data):
        """
        Update todo.
        """
        tags = validated_data.pop('tags',None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags,instance)
                
        instance.save()
        return instance
    

class TodoDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for todo details.
    """
    class Meta(TodoSerializer.Meta):
        fields = TodoSerializer.Meta.fields + ['complete','tags']


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student.
    """
    class Meta:
        model = Student
        fields = ['id','first_name', 'last_name', 'email','roll_number','mobile']
        read_only_fields = ['id']

    def create(self, validated_data):
        """
        Create and return a new student.
        """
        return Student.objects.create(**validated_data)

    def validate_first_name(self, value):
        """
        Validate the first name.
        """
        if value == "":
            raise serializers.ValidationError("Please enter a first name.")
        elif len(value) <= 4:
            raise serializers.ValidationError("First name must be at least 4 characters")
        return value
    
    def validate_roll_number(self, value):
        """
        validate roll number.
        """
        if value <= 10:
            raise serializers.ValidationError("Invalid roll number")
        return value
    
