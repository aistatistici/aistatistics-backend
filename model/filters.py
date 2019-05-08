from rest_framework_filters import filterset

from .models import DataSet


class DataSetFilter(filterset.FilterSet):

    class Meta:
        model = DataSet
        fields = {
            'id': '__all__',
            'name': '__all__',
        }
