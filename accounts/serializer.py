from rest_framework.validators import UniqueValidator

from accounts.models import Account
from rest_framework import serializers

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user_id')