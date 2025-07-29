from netbox.api.routers import NetBoxRouter
from . import views

router = NetBoxRouter()
router.register('profiles', views.ProfileViewSet)
router.register('flexapplications', views.FlexApplicationViewSet)
router.register('l4applications', views.L4ApplicationViewSet)
router.register('mtlsapplications', views.mTLSApplicationViewSet)
urlpatterns = router.urls