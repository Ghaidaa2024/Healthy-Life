from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_At = models.DateTimeField(auto_now_add=True, null=True)
    updated_At = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True