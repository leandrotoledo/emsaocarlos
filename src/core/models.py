from django.contrib import admin
from django.db import models

class Linha(models.Model):
	linha 	 = models.CharField(max_length=255)
	link     = models.CharField(max_length=255)
	nome 	 = models.CharField(max_length=255)
	origem   = models.CharField(max_length=255)
	destino  = models.CharField(max_length=255)
	via      = models.CharField(max_length=255)
	ida      = models.CharField(max_length=255)
	volta    = models.CharField(max_length=255)
	# TODO: horarios

#admin.site.register(Linha)
