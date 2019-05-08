from rest_framework.decorators import api_view

from utility.views import SerializerDispachViewSet

from .models import DataSet
from .filters import DataSetFilter
from .serializers import DataSetSerializer, PostDataSetSerializer


class DataSetView(SerializerDispachViewSet):

    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    serializer_action_classes = {
        'GET': DataSetSerializer,
        'POST': PostDataSetSerializer,
        'PATCH': PostDataSetSerializer,
    }
    filter_class = DataSetFilter


@api_view(['POST'])
def train_view():
    pass


@api_view(['POST'])
def split_view():

    pass


@api_view(['POST'])
def predict_view():

    pass
