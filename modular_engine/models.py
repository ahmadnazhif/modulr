from django.db import models

class Module(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_installed = models.BooleanField(default=False)
    installed_at = models.DateTimeField(null=True, blank=True)
    upgraded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
