import django_filters
from .models import XMLFile, NFe

class XMLFileFilter(django_filters.FilterSet):
    class Meta:
        model = XMLFile
        fields = {
            "dt_updated": ["gt", "lt", "exact", "gte", "lte"],
            "id": ["exact"],
            "user": ["exact"],
        }

class DatasFilter(django_filters.FilterSet):
    class Meta:
        model = NFe
        fields = {
            "id": ["exact"],
            "user": ["exact"],
            "emit_cnpj" : ["exact"],
            "dest_cnpj" : ["exact"],
        }    