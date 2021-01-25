from rest_framework import serializers
from .models import (XMLFile, NFe)
from .scripts import get_nfe_info
#import requests


class NFeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFe
        fields = (
            'id',
            'nfe_id',
            'emit_cnpj',
            'emit_name',
            'dest_cnpj',
            'dest_name',
            'valor_original_total',
            'xml',
            'dt_creation',
            'dt_updated',
        )


class XMLSerializer(serializers.ModelSerializer):

    class Meta:
        model = XMLFile
        fields = (
            'id',
            'xml',
            'dt_creation',
            'dt_updated',
        )

    def create(self, validated_data):
        xml = XMLFile.objects.create(**validated_data)
        nfe_info = get_nfe_info(xml)
        NFe.objects.create(xml=xml, nfe_id=nfe_info['nfe_id'], emit_cnpj=nfe_info['emit_cnpj'],
                           emit_name=nfe_info['emit_name'], dest_cnpj=nfe_info['dest_cnpj'], dest_name=nfe_info['dest_name'], valor_original_total=nfe_info['valor_original_total'])
        return xml
