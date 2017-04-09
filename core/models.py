from django.conf import settings
from django.db import models

# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks')
    done_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='done_tasks')

    @property
    def is_done(self):
        return bool(self.done_by)