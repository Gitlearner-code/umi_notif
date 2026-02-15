from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('recommandation.urls')),   # home view at /
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
]
