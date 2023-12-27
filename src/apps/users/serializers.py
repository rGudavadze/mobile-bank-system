from rest_framework import serializers
from models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['__all__']
        read_only_fields = ['id', 'created_at', 'deleted', 'last_login', 'updated_at']
        write_only_fields = ['password']


