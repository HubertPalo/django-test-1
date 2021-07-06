from django.db import models
# constructor?
# class Alerta (log)
# recibir alerta
# logica servidor para 

class Trap(models.Model):
    # location = models.CharField(max_length=100) - lat long
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=150)
    last_detected_movement_date = models.DateTimeField()
    last_photo_taken_link = models.CharField(max_length=200)
    last_video_taken_link = models.CharField(max_length=200)
    door_state = models.CharField(max_length=6) # OPEN CLOSED -> 2+?
    # inhibir notificaciones por un tiempo - date()

class Alert(models.Model):
    trap = models.ForeignKey(Trap, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    detected_at = models.DateTimeField()
    classified_as = models.CharField(max_length=5) # TRUE-P - FALSE-P
    
class Media(models.Model):
    trap = models.ForeignKey(Trap, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    type = models.CharField(max_length=5)
    link = models.CharField(max_length=100)
    bytes = models.IntegerField()
    seconds_length = models.SmallIntegerField(default=0)
    detected = models.BooleanField(default=False)
# tiene o no jabali

class Camera(models.Model):
    code = models.CharField(max_length=20)
    camera_description = models.CharField(max_length=100)
    last_image_link = models.CharField(max_length=200)
    state = models.CharField(max_length=3, default='OFF') # ON OFF
    
    def __str__(self):
        return self.code
    
    class Meta:
        ordering = ['code']





# class ImageDetail(models.Model):
#     desc = 
