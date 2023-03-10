from rest_framework import serializers
from .models import Book, Follow
from copies.models import Copy
from rest_framework.response import Response


class BookSerializer(serializers.ModelSerializer):
    copies = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "pages", "author", "publisher", "followers", "copies"]
        read_only_fields = ["id", "followers", "copies"]

    def get_copies(self, obj):
        return Copy.objects.filter(book=obj).count()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "id",
            "book",
        ]
        read_only_fields = [
            "id",
            "book",
        ]
