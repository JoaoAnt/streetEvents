from django.contrib.gis.db import models

STATE = ["TO_VALIDATE", "VALIDATED", "RESOLVED"]
CATEGORIES = ['CONSTRUCTIONS', 'SPECIAL_EVENT', 'INCIDENT', 'WEATHER_CONDITION', 'ROAD_CONDITION']

STATE_CHOICES = sorted([(item.replace("_"," ").title(), item) for item in STATE])
CATEGORIES_CHOICES = sorted([(item.replace("_"," ").title(), item) for item in CATEGORIES])

class Event(models.Model):
    description = models.CharField(max_length=500, blank=True, default='')
    location = models.PointField(null=True, blank=True)

    owner = models.ForeignKey('auth.User', related_name='events', on_delete=models.CASCADE)

    state = models.CharField(choices=STATE_CHOICES, default='To Validate', max_length=100)
    category = models.CharField(choices=CATEGORIES_CHOICES, default='Incident', max_length=100)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)

    def __repr__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
