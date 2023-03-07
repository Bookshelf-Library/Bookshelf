from rest_framework import serializers
from .models import Copy, Loan


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "is_avaliable", "book"]
        read_only_fields = ["id", "book", "is_avaliable"]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "is_active", "loaned_at", "deliver_in", "deliver_at", "copy", "account"]
        read_only_fields = ["id", "copy", "loaned_at", "deliver_in", "deliver_at", "account", "is_active"]
