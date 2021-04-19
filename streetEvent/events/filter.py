import django_filters
import math
from events.models import Event

class InsideRadiusLocation(filters.BaseFilterBackend):

    def get_inside(self, queryset, point, radius):
        if radius <= 0:
            return None
        else:
            insidecircle = []
            xcenter = point[0]
            ycenter = point[1]
            
            for i in range(len(Event.location)):
                xlocation = Event.points[i][0]
                ylocation = Event.points[i][1]
                if math.sqrt(abs(xlocation - xcenter)**2 + abs(ylocation - ycenter)**2) < radius:
                    insidecircle.append(i)
            return queryset.filter(index=insidecircle)