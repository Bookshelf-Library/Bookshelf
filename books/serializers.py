from rest_framework import serializers
from .models import Book, Follow


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "pages", "author", "publisher", "account"]
        read_only_fields = ["id", "account"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "book", "account"]
        read_only_fields = ["id", "book", "account"]
