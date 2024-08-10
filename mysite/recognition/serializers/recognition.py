from rest_framework import serializers

from mysite.recognition.models import Face

class FaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Face
        fields = ['id']

