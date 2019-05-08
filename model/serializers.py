import serpy

from rest_framework.serializers import ModelSerializer

from .models import DataSet


class DataSerSerializer(serpy.Serializer):

    id = serpy.Field()
    file = serpy.MethodField('get_file')
    model = serpy.MethodField('get_model')
    column_info = serpy.Field()
    train_info = serpy.Field()

    def get_file(self, dataset):
        pass

    def get_model(self, dataset):

        pass


class PostDataSetSerializer(ModelSerializer):

    class Meta:
        model = DataSet
        fields = ('name', 'file_path')

