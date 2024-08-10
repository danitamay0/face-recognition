from mysite.models import TimeStampMixin
from django.db import models
from clients.models import Client
from uuid import uuid4

class StatusFace(models.TextChoices):
        ACT = "ACTIVE", "Activo"
        DIS = "DESACTIVE", "Desactivado"

def face_directory_path(instance, filename):
    file_name = filename
    file_extension = file_name.split('.')[-1]
    print(file_extension, "file_extension")
    print(instance.face.id, "instance.facee")
    print(instance.id, "instance.id")
    
    return 'image/{0}/{1}.{2}'.format(instance.face.id, instance.id, file_extension)
    
class Face(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(Client, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    metadata =  models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=80,
        choices=StatusFace.choices,
        default=StatusFace.ACT)
   
    class Meta:
        verbose_name = "Rostro"
        verbose_name_plural = "Rostros"
    
    def __str__(self):
        return self.name

 
 
class FaceTraining(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    face = models.ForeignKey(Face, models.CASCADE)
    image=models.ImageField( upload_to=face_directory_path , verbose_name='Imagen')   
    face_encoding = models.TextField(blank=True)
    
    
def face_predict_path(instance, filename):
    file_name = filename
    file_extension = file_name.split('.')[-1]
    
    return 'predictions/{0}/.{1}'.format(instance.client.id, instance.id, file_extension)
    
    
class FacePredict(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    found_face = models.BooleanField(default=False)
    face = models.ForeignKey(Face, models.CASCADE, null=True, blank=True )
    client = models.ForeignKey(Client, models.CASCADE)
    image=models.ImageField( upload_to=face_predict_path , verbose_name='Imagen', null=True)   

    class Meta:
        verbose_name = "Historial de predicción"
        verbose_name_plural = "Historial de predicciones"