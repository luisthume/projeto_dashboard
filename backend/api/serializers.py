from rest_framework import serializers
from .models import (XMLFile, NFe, User, CNAE, NCM)
from .scripts import get_nfe_info
from django.db.models import Sum, Avg, Count
import os
# import requests


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'password',
                  'name',
                  'last_name'
                  )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CNAESerializer(serializers.ModelSerializer):

    class Meta:
        model = CNAE
        fields = (
            'id',
            'cnae',
            'nfe'
        )


class NCMSerializer(serializers.ModelSerializer):

    class Meta:
        model = NCM
        fields = (
            'id',
            'ncm',
            'nfe'
        )        


class NFeSerializer(serializers.ModelSerializer):
    nfe_cnae = CNAESerializer(many=True)
    nfe_ncm = NCMSerializer(many=True)
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
            'exit_date',
            'venc_dates',
            'nfe_cnae',
            'nfe_ncm',
            'xml',
        )

        
    def create(self,validated_data):
        cnaes_data = validated_data.pop('nfe_cnae')
        nfe = NFe.objects.create(**validated_data)
        for cnae_data in cnaes_data:
            CNAE.objects.create(nfe=nfe, **cnae_data)
        return nfe


class XMLSerializer(serializers.ModelSerializer):
    xml_info = NFeSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = XMLFile
        fields = (
            'id',
            'user',
            'xml',
            'xml_info',
            'dt_creation',
            'dt_updated',
        )

    def create(self, validated_data):
        xml = XMLFile.objects.create(**validated_data)
        nfe_info = get_nfe_info(xml)
        user = validated_data['user']
        if len(NFe.objects.filter(nfe_id=nfe_info['nfe_id'], user=user)) > 0:
            os.remove(str(xml))
            xml.delete()
            raise serializers.ValidationError(
                '{} NFe already in system'.format(nfe_info['nfe_id']))
        else:
            try:
                nfe = NFe.objects.create(xml=xml, nfe_id=nfe_info['nfe_id'], emit_cnpj=nfe_info['emit_cnpj'],
                                   emit_name=nfe_info['emit_name'], 
                                   dest_cnpj=nfe_info['dest_cnpj'], 
                                   dest_name=nfe_info['dest_name'], 
                                   valor_original_total=nfe_info['valor_original_total'], 
                                   exit_date=nfe_info['exit_date'],
                                   user_id=xml.user_id,
                                   venc_dates=nfe_info['venc_dates'],
                                   )

                CNAE.objects.create(nfe=nfe, cnae=nfe_info['cnae'], user=nfe.user)
                for i in nfe_info['ncm']:
                    NCM.objects.create(nfe=nfe, ncm=i, user=nfe.user)

            except IndexError:#TypeError:
                os.remove(str(xml))
                xml.delete()
                raise serializers.ValidationError(
                    '{} not parsable'.format(nfe_info['nfe_id']))                
        return xml


class DataSerializer(serializers.ModelSerializer):
    valor_total = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    operation_mean = serializers.SerializerMethodField()
    cnae =serializers.SerializerMethodField()
    ncm =serializers.SerializerMethodField()

    class Meta:
        model = NFe
        fields = (
            'emit_cnpj',
            'emit_name',
            'dest_cnpj',
            'dest_name',
            'valor_total',
            'operation_mean',
            'dates',
            'venc_dates',
            'cnae',
            'ncm',
        )

    def get_valor_total(self, instance):
        emit_cnpj = instance.emit_cnpj
        dest_cnpj = instance.dest_cnpj

        obj_nfe = NFe.objects.filter(emit_cnpj=emit_cnpj, dest_cnpj=dest_cnpj)
        return obj_nfe.aggregate(Sum('valor_original_total'))['valor_original_total__sum']

    def get_operation_mean(self, instance):
        emit_cnpj = instance.emit_cnpj
        dest_cnpj = instance.dest_cnpj

        obj_nfe = NFe.objects.filter(emit_cnpj=emit_cnpj, dest_cnpj=dest_cnpj)
        return obj_nfe.aggregate(Avg('valor_original_total'))['valor_original_total__avg']

    def get_dates(self, instance):
        emit_cnpj = instance.emit_cnpj
        dest_cnpj = instance.dest_cnpj

        obj_nfe = NFe.objects.filter(emit_cnpj=emit_cnpj, dest_cnpj=dest_cnpj)
        return (tuple(obj_nfe.values_list('exit_date', flat=True)))

    def get_cnae(self, instance):
        nfe_id = instance.id

        obj_cnae = CNAE.objects.filter(nfe=nfe_id)
        return list(set([i for i in obj_cnae.values_list('cnae', flat=True)]))

    def get_ncm(self, instance):
        nfe_id = instance.id

        obj_ncm = NCM.objects.filter(nfe=nfe_id)
        return list(set([i for i in obj_ncm.values_list('ncm', flat=True)]))