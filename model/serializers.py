import serpy
import os

from rest_framework import serializers

from utility.serializers import ContextSerializer

from project.models import Project
from .models import DataSet


class DataSetSerializer(ContextSerializer):

    id = serpy.Field()
    file = serpy.MethodField('get_file')
    model = serpy.MethodField('get_model')
    column_info = serpy.Field()
    train_info = serpy.Field()

    def get_file(self, dataset):

        return self.context['view'].request.build_absolute_uri(
            dataset.file_path.url) if self.context else dataset.file_path.url

    def get_model(self, dataset):

        return self.context['view'].request.build_absolute_uri(
            dataset.model_path.url) if self.context else dataset.model_path.url


class PostDataSetSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    column_info = serializers.JSONField(required=False)
    train_info = serializers.JSONField(required=False)

    def validate_file_path(self, path):

        valid_file_extensions = ['.csv', '.xlsx']
        filename, file_extension = os.path.splitext(path._get_name())
        if file_extension not in valid_file_extensions:
            raise serializers.ValidationError("Invalid file extension")
        return path

    class Meta:
        model = DataSet
        fields = ('name', 'file_path', 'column_info', 'train_info', 'project')

