from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Street Events",
      default_version='v1',
      description="""One weekend backend django with PostGis Project.
      
Where any one can see an event, loggin users can create an event, owner and admins can update or delete the event and admins can change is state.""",
      contact=openapi.Contact(email="joaoantant@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('events.urls')),
]



urlpatterns += [
    path('swagger.json', schema_view.without_ui(cache_timeout=0)),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0)),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0)),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
