"""sptest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from sptest.friends import friends_views, subscribe_views

schema_view = get_schema_view(
    openapi.Info(
        title='Singapore Power Test for Full-Stack Developer',
        default_version='v1',
        description='Singapore Power Test for Full-Stack Developer',
        contact=openapi.Contact(email="st_lim@stlim.net"),
        licence=openapi.License(name="Apache-2.0")
    ),
    public=True
)

urlpatterns = [
    url(r'^friends/$', friends_views.FriendsView.as_view()),
    url(r'^subscribe/$', subscribe_views.SubscribeView.as_view()),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
