from rest_framework import serializers
from .models import (XMLFile, NFe, User)
from .scripts import get_nfe_info
import os
#import requests


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
        )


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
        if len(NFe.objects.filter(nfe_id=nfe_info['nfe_id'])) > 0:
            os.remove(str(xml))
            xml.delete()
            raise serializers.ValidationError(
                '{} NFe already in system'.format(xml))
            
        else:
            NFe.objects.create(xml=xml, nfe_id=nfe_info['nfe_id'], emit_cnpj=nfe_info['emit_cnpj'],
                               emit_name=nfe_info['emit_name'], dest_cnpj=nfe_info['dest_cnpj'], dest_name=nfe_info['dest_name'], valor_original_total=nfe_info['valor_original_total'], user_id=xml.user_id)
        return xml
