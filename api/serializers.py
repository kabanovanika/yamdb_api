from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Comment, Review, Title, Category, Genre
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class CategoryField(serializers.SlugRelatedField):

    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreField(serializers.SlugRelatedField):

    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = GenreField(
        slug_field='slug', 
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    review = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    def validate_score(self, score):
        if score < 1 or score > 10:
            raise serializers.ValidationError("Оценка должна между 1 и 10.")
        return score

    class Meta:
        model = Review
        fields = '__all__'
