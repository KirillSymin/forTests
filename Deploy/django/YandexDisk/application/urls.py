from django.contrib import admin
from django.urls import path, include

from application.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('entity.urls', namespace='entity')),
]

if DEBUG:
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
