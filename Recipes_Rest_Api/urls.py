from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Recipes_Rest_Api import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_recipes.urls'))
]

# settings for static files if Debug is True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
