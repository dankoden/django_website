from rest_framework import serializers
from .models import Category,News



class NewsSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ("views",)
