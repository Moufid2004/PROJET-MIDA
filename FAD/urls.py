from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from api.views import ProduitsViewSet, CatégorieViewSet, FermeViewSet, CommandeViewSet  

router = routers.DefaultRouter()
router.register('Produits', ProduitsViewSet)
router.register('Catégorie', CatégorieViewSet)
router.register('Ferme', FermeViewSet)  
router.register('Commande', CommandeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
