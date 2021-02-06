
from rest_framework import pagination
from rest_framework.response import Response

class DatasPagination(pagination.PageNumberPagination):
    page_size = 10000
    def get_paginated_response(self, data):
        seen = []
        uniques = []
        for i in data:
            values = list(i.values())[:-1]
            if not values in seen:
                seen.append(values)
                uniques.append(i)      
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': len(uniques),
            'results': uniques
        })

class DatasCSVPagination(pagination.PageNumberPagination):
    page_size = 10000
    def get_paginated_response(self, data):
        seen = []
        uniques = []
        for i in data:
            values = list(i.values())[:-1]
            if not values in seen:
                seen.append(values)
                uniques.append(i)

        return Response(uniques)        