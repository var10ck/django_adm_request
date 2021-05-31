"""django_adm_request URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static, serve
from django.views.generic import RedirectView

urlpatterns = [
                  re_path(r'^jet/', include('jet.urls', 'jet')),
                  re_path(r'^jet/dashboard', include('jet.dashboard.urls', 'jet-dashboard')),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_fw')),
                  path('', RedirectView.as_view(url='admin/')),
                  path('admin/', admin.site.urls),
                  re_path(r'^report_builder/', include('report_builder.urls')),
                  re_path(r'^api/adm_request/',
                          include(('adm_request.api_urls', 'adm_request'), namespace='adm_request_api')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
