from rest_framework_filters import filters

from .models import Project


class ProjectFilter(filters.FilterSet):

    class Meta:
        model = Project
        fields = {
            'id': '__all__',
            'name': '__all__',
        }
