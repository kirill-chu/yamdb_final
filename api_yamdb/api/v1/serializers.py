"""Serializers for API app."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from .validators import regexp_validator

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """A serializer for Category instances."""

    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects)]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """A serializer for Genre instances."""

    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Genre.objects)]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """A serializer for read/destroy Title instances."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CreateUpdateTitleSerializer(TitleSerializer):
    """A serializer for create/update Title instances."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects, many=True
    )

    class Meta:
        fields = ('name', 'year', 'description', 'category', 'genre')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects,
                fields=('name', 'year', 'category')
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return TitleSerializer(instance, context=context).data


class CurrentTitleDefault:
    """Function receive title id from path parameter."""

    requires_context = True

    def __call__(self, serializer_field):
        context = serializer_field.context['request'].parser_context
        return get_object_or_404(
            Title, id=context.get('kwargs').get('title_id'))


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review instance."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        fields = '__all__'
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return Review.objects.create(**validated_data)


class CurrentReviewDefault:
    """Function receive review id from path parameter."""

    requires_context = True

    def __call__(self, serializer_field):
        context = serializer_field.context['request'].parser_context
        return get_object_or_404(
            Review, title__id=context.get('kwargs').get('title_id'),
            id=context.get('kwargs').get('review_id'))


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment instance."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    review = serializers.HiddenField(default=CurrentReviewDefault())

    class Meta:
        fields = '__all__'
        model = Comment

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return Comment.objects.create(**validated_data)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[regexp_validator],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Использование имени {value} '
                f'в качестве username запрещено.'
            )
        return value

    class Meta:
        fields = (
            'username',
            'email',
        )
        model = User


class NewTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[regexp_validator],
    )

    class Meta:
        fields = (
            'username',
            'confirmation_code',
        )
        model = User


class UserSerializer(serializers.ModelSerializer):
    """User serializer for Users App."""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class MeSerializer(serializers.ModelSerializer):
    """User serializer for Users App."""

    username = serializers.CharField(
        max_length=150,
        validators=[regexp_validator],
        required=False
    )
    email = serializers.EmailField(
        max_length=254,
        required=False
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        read_only_fields = ('role',)
