from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


from banking.views import page_not_found

urlpatterns = [
    path('', RedirectView.as_view(url='banking/', permanent=True)),
    path('admin/', admin.site.urls),
    path('banking/', include('banking.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

handler404 = page_not_found
