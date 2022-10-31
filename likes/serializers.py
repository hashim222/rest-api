from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'post', 'created_at'
        ]

    def create(self, validated_data):
        try:
            super_var = super().create(validated_data)
            # print('You clicked once: 🤞', super_var)
            return super_var
        except IntegrityError:
            # print('You clicked twice: 😅')
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
