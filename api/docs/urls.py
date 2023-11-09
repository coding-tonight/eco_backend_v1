from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.permissions import AllowAny

from . import views


schema_view = get_schema_view(
    openapi.Info(
        title="Bhumi Forever Fashion Api",
        default_version='v.1.0',
        description="Welcome to the Api Documentation"
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('api/swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),

    path('api/redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('', views.DocsApiView.as_view())
]
