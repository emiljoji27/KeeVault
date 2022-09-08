from django.contrib import admin
from . import models

admin.site.register(models.PasswordModel)
admin.site.register(models.Notes)