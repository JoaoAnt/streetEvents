from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from events.models import Event
from events.permissions import IsOwnerAdminOrReadOnly
from events.serializers import (AdminEventSerializer, EventSerializer,
                                UserSerializer)


class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    
    **Permissions:** admins can change the state, owner and admins can update events, requires login to create a 
    new event, any person can view the events.

    **Filters:** `state`, `owner` and `category` in the Filters button, type`lat`, `lng` in the url to order by 
    distance, `rnd` (in Km) can also be added to this two to filter the distance. The filters can be used simultaneosly.

    Example: `http://127.0.0.1:8000/events/?lat=20&lng=20&rnd=2000` or `http://127.0.0.1:8000/events/?lat=2&lng=23&state=To+Validate&owner=&category=` 
    """

    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state', 'owner', 'category']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminEventSerializer
        return EventSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        latitude = self.request.query_params.get('lat')
        longitude = self.request.query_params.get('lng')
        radius = self.request.query_params.get('rnd')

        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(' + str(longitude) + ' ' + str(latitude) + ')', srid=4326)
            radiusKm = radius+'000' # Radius in meters, times 1000 to be km, due to radius being a string is easyer to just had the 3 zeros like this
            qs = qs.annotate(distance=Distance('location', pnt)).filter(distance__lte=radiusKm).order_by('distance')
            print(qs)

        elif latitude and longitude:
            pnt = GEOSGeometry('POINT(' + str(longitude) + ' ' + str(latitude) + ')', srid=4326)
            qs = qs.annotate(distance=Distance('location', pnt)).order_by('distance')

        return qs


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.

    **Permissions:** any person can view this pages.

    **Filters:** Search Filter for both `username` and `email`.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
