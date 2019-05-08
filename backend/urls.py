"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from rest_framework import routers

import project.urls as project_routes
import model.urls as model_routes

router = routers.DefaultRouter()

routes = [
    project_routes.routes,
    model_routes.routes
]

for route_list in routes:
    for r in route_list:
        base_name = None if len(r) <= 2 else r[2]
        router.register(r[0], r[1], base_name=base_name)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
