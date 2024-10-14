from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['uuid', 'description', 'amount', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'created_at', 'updated_at', 'created_by']
