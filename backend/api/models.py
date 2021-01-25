from django.db import models
from django.conf import settings

# Create your models here.


class Base(models.Model):
    dt_creation = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class XMLFile(Base):
    xml = models.FileField(blank=True, upload_to="xmls/")

    class Meta:
        verbose_name = 'XML'
        verbose_name_plural = 'XMLs'
        ordering = ['id']

    def __str__(self):
        return f'{self.xml}'


class NFe(Base):
    nfe_id = models.CharField(max_length=50)
    emit_cnpj = models.CharField(max_length=50)
    emit_name = models.CharField(max_length=50)
    dest_cnpj = models.CharField(max_length=50)
    dest_name = models.CharField(max_length=50)
    valor_original_total = models.CharField(max_length=50)
    xml = models.ForeignKey(XMLFile, related_name='xml_info', on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        verbose_name = 'NFe'
        verbose_name_plural = 'NFes'
        ordering = ['id']

        def __str__(self):
            return f'{self.nfe_id}'
