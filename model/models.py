import os
import datetime

from django.db import models

from django.contrib.postgres.fields import JSONField

# Create your models here.


def upload_file_location(instance, filename):

    filename, file_extension = os.path.splitext(filename)
    return "datasets/{0}/{1}{2}".format(instance.name, datetime.datetime.now(), file_extension)


def upload_model_location(instance, filename):

    filename, file_extension = os.path.splitext(filename)
    return "datasets/{0}/models/{1}{2}".format(instance.name, datetime.datetime.now(), file_extension)


class DataSet(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    file_path = models.FileField(upload_to=upload_file_location)
    model_path = models.FileField(upload_to=upload_model_location)
    column_info = JSONField()
    train_info = JSONField()
    project = models.ForeignKey('project.Project', related_name='data_sets', on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.name}"
