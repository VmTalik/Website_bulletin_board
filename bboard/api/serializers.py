from rest_framework import serializers
from main.models import Bb


class BbSerializer(serializers.ModelSerializer):
    """Класс - сериализатор, формирует список объявлений"""

    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')


class BbDetailSerializer(serializers.ModelSerializer):
    """Класс-сериализатор, выдает сведения об объявлении"""

    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at',
                  'contacts', 'image')
