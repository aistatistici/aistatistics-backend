# Generated by Django 2.2.1 on 2019-05-08 21:53

from django.db import migrations, models
import model.models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='model_path',
            field=models.FileField(null=True, upload_to=model.models.upload_model_location),
        ),
    ]
