from django.db import models


class Image(models.Model):
    filename = models.CharField(max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return self.filename
