from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('vendors/', include('vendors.urls')),
    path('people/', include('people.urls')),
    path('', RedirectView.as_view(url='/vendors/', permanent=False)),
]
