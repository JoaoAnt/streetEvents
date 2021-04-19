from django.contrib.auth.models import User
from rest_framework import serializers

from events.models import Event


class UserSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail', read_only=True)
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['url','id', 'username', 'email', 'events', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class EventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    distance = serializers.DecimalField(source='distance.km', max_digits=10, decimal_places=2, required=False, read_only=True)
    class Meta:
        model = Event
        fields = ['url','id', 'description', 'owner', 'location', 'owner', 'state', 'category', 'distance']
        read_only_fields = ['state']

class AdminEventSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    distance = serializers.DecimalField(source='distance.km', max_digits=10, decimal_places=2, required=False, read_only=True)

    class Meta:
        model = Event
        fields = ['url','id', 'description', 'owner', 'location', 'owner', 'state', 'category', 'distance']