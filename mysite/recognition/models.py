from mysite.models import TimeStampMixin
from django.db import models
from clients.models import Client
from uuid import uuid4

class StatusFace(models.TextChoices):
        ACT = "ACTIVE", "Activo"
        DIS = "DESACTIVE", "Desactivado"

    
class Face(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(Client, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='images')   
    metadata =  models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=80,
        choices=StatusFace.choices,
        default=StatusFace.ACT)
    face_encoding = models.TextField(blank=True)

    def save(self):
        difFecha = self.disponibleMAC - self.recibidoVRD
        self.diferencia = difFecha.seconds
        super (Distribucion, self).save()
        
    class Meta:
        verbose_name = "Rostros"
        verbose_name_plural = "Rostro"
 