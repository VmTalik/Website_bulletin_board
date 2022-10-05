from rest_framework import serializers
from main.models import Bb
from main.models import Comment


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


class CommentSerializer(serializers.ModelSerializer):
    """Класс-сериализатор, выдает список комментариев
    и добавляет новый комментарий"""

    class Meta:
        model = Comment
        fields = ('bb', 'author', 'content', 'created_at')
