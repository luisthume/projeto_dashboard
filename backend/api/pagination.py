
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        #data = set( val for dic in data for val in dic.values())
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
            'count': self.page.paginator.count,
            'results': uniques
        })