from rest_framework_filters import filterset

from .models import Project


class ProjectFilter(filterset.FilterSet):

    class Meta:
        model = Project
        fields = {
            'id': '__all__',
            'name': '__all__',
        }
