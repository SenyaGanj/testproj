from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings


class File(models.Model):
    file = models.FileField(
        verbose_name='File',
        validators=[FileExtensionValidator(allowed_extensions=['py'])]
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='files',
        verbose_name='Created by',
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Log.objects.create(file=self)


class Log(models.Model):
    STATUS_NEW = 'new'
    STATUS_PROCESS = 'processing'
    STATUS_DONE = 'done'

    created = models.DateTimeField(verbose_name='Created at', auto_now_add=True, editable=False)
    updated = models.DateTimeField(verbose_name='Updated at', auto_now=True, editable=False)
    file = models.ForeignKey(
        File,
        related_name='logs',
        verbose_name='Logs',
        on_delete=models.CASCADE,
    )
    status = models.CharField(verbose_name='Statuses', default=STATUS_NEW, max_length=20, choices=(
        (STATUS_NEW, STATUS_NEW),
        (STATUS_PROCESS, STATUS_PROCESS),
        (STATUS_DONE, STATUS_DONE),
    ))
    result = models.TextField(verbose_name='Report', blank=True)
    is_sent_to_email = models.BooleanField(verbose_name='Sent to mail', default=False)
