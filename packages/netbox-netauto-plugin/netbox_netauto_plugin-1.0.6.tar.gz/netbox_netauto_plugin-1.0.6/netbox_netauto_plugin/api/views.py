from netbox.api.viewsets import NetBoxModelViewSet
from .. import models, filtersets
from . import serializers

class ProfileViewSet(NetBoxModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    filterset_class = filtersets.ProfileFilterSet

class FlexApplicationViewSet(NetBoxModelViewSet):
    queryset = models.FlexApplication.objects.all()
    serializer_class = serializers.FlexApplicationSerializer
    # filterset_class = filtersets.FlexApplicationFilterSet

    def perform_destroy(self, instance):
        instance.api_delete()

class L4ApplicationViewSet(NetBoxModelViewSet):
    queryset = models.L4Application.objects.all()
    serializer_class = serializers.L4ApplicationSerializer
    # filterset_class = filtersets.L4ApplicationFilterSet

    def perform_destroy(self, instance):
        instance.api_delete()

class mTLSApplicationViewSet(NetBoxModelViewSet):
    queryset = models.mTLSApplication.objects.all()
    serializer_class = serializers.mTLSApplicationSerializer
    # filterset_class = filtersets.mTLSApplicationFilterSet

    def perform_destroy(self, instance):
        instance.api_delete()