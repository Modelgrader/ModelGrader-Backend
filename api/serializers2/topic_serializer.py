from rest_framework import serializers
from ..models import *

class GetTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['name', 'description', 'image_url']