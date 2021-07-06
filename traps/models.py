from django.db import models

class Trap(models.Model):
    # ubicacion ? (lat-long)
    # UC1
    last_detected_movement_date = models.DateField()
    # movement_detected = models.BooleanField()
    
    # camera
    last_photo_taken = models.CharField(max_length=200)
    last_video_taken = models.CharField(max_length=200)
    # media
    door_state = models.BooleanField()

    code = models.CharField(max_length=20)
    camera_description = models.CharField(max_length=100)
    last_image_link = models.CharField(max_length=200)
    
    def __str__(self):
        return self.code
    
    class Meta:
        ordering = ['code']
