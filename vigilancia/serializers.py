
from django.db.models import query_utils
from vigilancia.models import Alert, Camera, Trap
from rest_framework  import serializers


#*class CameraSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Camera
#        fields = ['id', 'code', 'camera_description', 'last_image_link']

class AlertSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    trap = serializers.PrimaryKeyRelatedField(queryset=Trap.objects.all())
    created_at = serializers.DateTimeField()
    detected_at = serializers.DateTimeField()
    classified_as = serializers.CharField(max_length=5)
    def create(self, validated_data):
        return Alert.objects.create(**validated_data)

class TrapSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=False, allow_blank=True, max_length=10)
    description = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_detected_movement_date = serializers.DateTimeField()
    last_photo_taken_link = serializers.CharField(required=False, allow_blank=True, max_length=200)
    last_video_taken_link = serializers.CharField(required=False, allow_blank=True, max_length=200)
    door_state = serializers.CharField(max_length=6)
    def create(self, validated_data):
        return Trap.objects.create(**validated_data)

class MediaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    trap = serializers.PrimaryKeyRelatedField(queryset=Trap.objects.all())
    date = serializers.DateTimeField()
    type = serializers.CharField(max_length=5)
    link = serializers.CharField(max_length=100)
    bytes = serializers.IntegerField()
    seconds_length = serializers.IntegerField(default=0)
    detected = serializers.BooleanField(default=False)

class CameraSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=False, allow_blank=True, max_length=20)
    camera_description = serializers.CharField(required=False, allow_blank=True, max_length=100)
    last_image_link = serializers.CharField(required=False, allow_blank=True, max_length=200)
    
    def create(self, validated_data):
        return Camera.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.camera_description = validated_data.get('camera_description', instance.camera_description)
        instance.last_image_link = validated_data.get('last_image_link', instance.last_image_link)
        instance.save()
        return instance

class CameraOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.CharField()

class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']




