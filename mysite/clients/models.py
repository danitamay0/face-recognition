from mysite.models import TimeStampMixin
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Liscences(models.TextChoices):
        PEN = "PENDING", "Pendiente"
        ACT = "ACTIVE", "Activa"
        DIS = "DESACTIVE", "Desactivada"

    
class Client(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.TextField()
    token_auth = models.CharField(max_length=255, blank=True, null=True)
    license = models.CharField(
        max_length=50,
        choices=Liscences.choices,
        default=Liscences.PEN
    )
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
 