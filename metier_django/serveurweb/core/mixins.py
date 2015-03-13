#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http.response import JsonResponse
from django.core import serializers

class JSONResponseMixin(object):
    """
    classe de réponse en JSON
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        retourne HttpResponse au format JSON sans HTML
        """
        return JsonResponse(
            self.get_data(context),
            safe=False,
            **response_kwargs
        )

    def get_data(self, context):
        """
        utilise le sérialiseur JSON de Django pour l'envoi
        """
        return serializers.serialize('json', context)
