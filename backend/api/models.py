from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

# Create your models here.


class User(AbstractUser):
	username = models.CharField(blank=True, null=True, max_length=50)
	name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.EmailField(_('email address'), unique=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'name', 'last_name']

	def __str__(self):
		return "{}".format(self.email)


class Base(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    nfe_id = models.CharField(max_length=50, null=True)
    emit_cnpj = models.CharField(max_length=20, null=True)
    emit_name = models.CharField(max_length=150, null=True)
    dest_cnpj = models.CharField(max_length=20, null=True)
    dest_name = models.CharField(max_length=150, null=True)
    valor_original_total = models.FloatField(null=True)
    exit_date = models.DateTimeField(null=True)
    venc_dates = models.CharField(max_length=500, null=True)
    cnae = models.CharField(max_length=15, null=True)
    xml = models.ForeignKey(
        XMLFile, related_name='xml_info', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'NFe'
        verbose_name_plural = 'NFes'
        ordering = ['id']

        def __str__(self):
            return f'{self.nfe_id}'


class CNAE(Base):
    cnae = models.BigIntegerField(null=True)
    nfe = models.ForeignKey(
        NFe, related_name='nfe_cnae', on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        verbose_name = 'CNAE'
        verbose_name_plural = 'CNAEs'
        ordering = ['id']

    def __str__(self):
        return f'{self.cnae}.'


class NCM(Base):
    ncm = models.BigIntegerField(null=True)
    nfe = models.ForeignKey(
        NFe, related_name='nfe_ncm', on_delete=models.CASCADE, default=None, null=True)

    class Meta:
        verbose_name = 'NCM'
        verbose_name_plural = 'NCMs'
        ordering = ['id']

    def __str__(self):
        return f'{self.ncm}.'   
