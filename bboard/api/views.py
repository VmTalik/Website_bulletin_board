from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Bb
from .serializers import BbSerializer
from rest_framework.generics import RetrieveAPIView
from .serializers import BbDetailSerializer


@api_view(['GET'])
def bbs(request):
    """Функция-контроллер, которая выдает список объявлений"""
    if request.method == 'GET':
        bbs = Bb.objects.filter(is_active=True)[:10]
        serializer = BbSerializer(bbs, many=True)
        return Response(serializer.data)


class BbDetailView(RetrieveAPIView):
    """Класс-контроллер для вывода сведений о выбранном объявлении"""
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbDetailSerializer
