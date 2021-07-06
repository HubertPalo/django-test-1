from datetime import date
from email import message
from vigilancia.order_screenshot import Orders
from django.db.models.fields import DateField
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Camera, Trap
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import AlertSerializer, CameraOrderSerializer, CameraSerializer, MediaSerializer, TrapSerializer

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer

from ftplib import FTP
import json

from vigilancia import serializers
import vigilancia.services.send_email
import vigilancia.services.camera_service
import logging
from datetime import datetime
import os


logger = logging.getLogger("django")

@csrf_exempt
def report_alert(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        logger.info("Alerta detectada. Detalles: Armadilha %s, Detectado %s.", str(data['trap']), data['detected_at'])
        serializer = AlertSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message = 'Oi, a armadilha ' + str(data['trap']) + ' notificou movimento as ' + data['detected_at']
            print(message)
            vigilancia.services.send_email.send_gmail_test(str(data['trap']) )
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def camera_order(request):
    data = JSONParser().parse(request)
    serializer = CameraOrderSerializer(data=data)
    response = 'OK'
    orders_object = Orders()
    if serializer.is_valid():
        response = serializer.data
        response = Orders().take_screeshot()
    return JsonResponse(response, safe=False)

@csrf_exempt
def trap_general(request):
    """
    (GET) List all traps
    (POST) Create one trap
    """
    if request.method == 'GET':
        allObjects = Trap.objects.all()
        serializer = TrapSerializer(allObjects, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TrapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def trap_specific(request, pk):
    """
    (GET) Obtain the detail of one specific trap asdadas
    """
    data = JSONParser().parse(request)
    serializer = CameraSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def movement_detected(request):
    """
    (POST) Register movement detected in a trap
    """
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(request)
        # trap = Trap.objects.get(pk=trap_pk)
    except Trap.DoesNotExist:
        return HttpResponse(status=404)
    # trap = Trap()
    # trap.last_detected_movement_date = date()
    # Trap.objects.update(trap)
    return JsonResponse({'request': body}, status=201)

    data = JSONParser().parse(request)
    serializer = TrapSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def camera_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cameras = Camera.objects.all()
        serializer = CameraSerializer(cameras, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CameraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def take_photo(request, pk):
    try:
        camera = Camera.objects.get(pk=pk)
    except Camera.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'POST':
        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(base_folder, 'test.jpg')
        print('IMAGE PATH', image_path)
        file = open(image_path, 'rb')
        file_name = 'TRAP' + str(pk) + '-' + str(datetime.now().strftime("%Y%m%d-%H%M%S")) + '.jpg'
        #serializer = MediaSerializer(data={"trap": 1, "date": "2021-06-25T01:55:19"})
        #if serializer.is_valid():
        #    serializer.save()
        print(file.__dict__, file_name)
        vigilancia.services.camera_service.CameraService().upload_photo(file, file_name)
        return JsonResponse({"file_name": file_name})

@csrf_exempt
def camera_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        camera = Camera.objects.get(pk=pk)
    except Camera.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CameraSerializer(camera)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CameraSerializer(camera, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        camera.delete()
        return HttpResponse(status=204)

@csrf_exempt
def upload_photo(request):
    try:
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type) + " called {}".format(file_uploaded)
        response = "dir {}, dict {}, content_type {}".format(dir(file_uploaded), file_uploaded.__dict__, file_uploaded.content_type)
        
        session = FTP(host='maonamata.com.br', user='mnmdev@maonamata.com.br', passwd='mnmDev2021')
        # response = session.pwd()
        session.storbinary('STOR ' + file_uploaded._name, file_uploaded.file)
        #session.cwd('./../../public_html/pipe1/trapassets/trap1test/')
        session.quit()

        return HttpResponse(response)
    except Camera.DoesNotExist:
        return HttpResponse(status=404)

@csrf_exempt
def send_email(request):
    vigilancia.services.send_email.send_gmail_test(['darlinnep@gmail.com'], 'texto test')
    return HttpResponse('OK')

class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(response)

#def index(request):
#    list = Camera.objects.order_by('-id')[:5]
#    context = {'list': list}
#    return render(request, 'cameras/index.html', context)

#def detail(request, camera_id):
#    camera = get_object_or_404(Camera, pk=camera_id)
#    return render(request, 'cameras/detail.html', {'camera': camera})
