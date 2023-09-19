"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import SimpleRouter
from accounts.vews import RegisterView, LoginView
from fileman.views import FileListView, CreateFileView, UpdateFileView, DetailFileResultView
from fileman.api.v1.file import FileViewSet

router = SimpleRouter()
router.register('files', FileViewSet, basename='file_api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', FileListView.as_view(), name='file_list'),
    path('new/', CreateFileView.as_view(), name='create_file'),
    path('<pk>/', UpdateFileView.as_view(), name='file_detail'),
    path('result/<pk>/', DetailFileResultView.as_view(), name='file_result'),
    path('api/v1/', include(router.urls)),
]
