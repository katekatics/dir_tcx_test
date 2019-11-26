from django.db import models
from django.utils import timezone


# Create your models here.
class Incident(models.Model):
    DANGER = 'danger'
    WARNING = 'warning'
    SUCCESS = 'success'
    CRITICALITY_CHOICES = (
        (DANGER, 'danger'),
        (WARNING, 'warning'),
        (SUCCESS, 'success'),
    )
    store = models.CharField(max_length=16)
    created = models.DateTimeField(default=timezone.now)
    problem = models.TextField()
    incident = models.CharField(max_length=30)
    date_solved = models.DateTimeField(default=timezone.now)
    current_status = models.CharField(default='', max_length=255)
    criticality = models.CharField(max_length=7, choices=CRITICALITY_CHOICES)
    objects = models.Manager()
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Инциденты'
        verbose_name_plural = 'Инциденты'

    def __str__(self):
        return '[{0}][{1}] {2}'.format(self.store, self.criticality, self.problem)


class Message(models.Model):
    store = models.CharField(max_length=16, unique=True)
    body = models.TextField()
    objects = models.Manager()

    class Meta:
        ordering = ('-store',)
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.store

class Dirs(models.Model):
    sap = models.CharField(max_length=4)
    last_name = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=256, default='')
    otchestvo = models.CharField(max_length=256, default='')
    director = models.EmailField()

    class Meta:
        ordering = ('-sap',)
        verbose_name = 'Директора'
        verbose_name_plural = 'Директора'
    
    def __str__(self):
        return self.sap
