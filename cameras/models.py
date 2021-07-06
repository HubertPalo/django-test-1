from django.db import models

class Camera(models.Model):
    
    state = models.CharField(max_length=20) # 'ON' 'OFF'
    
    # UC2