from utility.views import SerializerDispachViewSet

from .models import Project
from .serializers import ProjectSerializer, PostProjectSerializer
from .filters import ProjectFilter


class ProjectViewSet(SerializerDispachViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    serializer_action_classes = {
        'GET': ProjectSerializer,
        'POST': PostProjectSerializer,
        'PATCH': PostProjectSerializer,
    }
    filter_class = ProjectFilter


