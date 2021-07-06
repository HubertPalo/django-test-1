from django.urls import path, include
from rest_framework import routers
from .views import UploadViewSet

from . import views

router = routers.DefaultRouter()
router.register(r'upload', UploadViewSet, basename="upload")

urlpatterns = [
    #path('', views.index, name='index'),
    #path('<int:camera_id>/', views.detail, name='detail'),
    path('cameras/', views.camera_list),
    path('cameras/<int:pk>/', views.camera_detail),
    path('photo/', views.upload_photo),
    path('movement/', views.movement_detected),
    path('cameras/uploadphoto', include(router.urls)),
    
    path('trap/', views.trap_general),
    path('order/', views.camera_order),
    path('email/', views.send_email),
    # 1
    path('alert/', views.report_alert),
    # 2
    #path('camera_on/', views.turn_camera_on),
    #path('camera_off/', views.turn_camera_off),
    # 3
    path('screenshot/<int:pk>/', views.take_photo),
    # 4

]