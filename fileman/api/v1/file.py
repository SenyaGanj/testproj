from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from fileman.models import File, Log


class FilePermissions(BasePermission):
    def has_object_permission(self, request, _, obj):
        return obj.created_by == request.user


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'created', 'updated', 'status', 'result', 'is_sent_to_email')


class FileSerializer(ModelSerializer):
    logs = LogSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('created_by',)


class FileViewSet(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated & FilePermissions,)
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.filter(created_by=self.request.user).prefetch_related('logs')
