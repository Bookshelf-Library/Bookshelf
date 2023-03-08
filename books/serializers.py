from rest_framework import serializers
from .models import Book, Follow
from copies.models import Copy


class BookSerializer(serializers.ModelSerializer):
    copies = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "pages", "author", "publisher", "account", "copies"]
        read_only_fields = ["id", "account", "copies"]
        depth = 1

    def get_copies(self, obj):
        return Copy.objects.filter(book=obj).count()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "book", "account"]
        read_only_fields = ["id", "book", "account"]
        depth = 1
