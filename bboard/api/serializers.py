from rest_framework import serializers
from main.models import Bb


class BbSerializer(serializers.ModelSerializer):
    """Класс - сериализатор, формирует список объявлений"""

    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')
