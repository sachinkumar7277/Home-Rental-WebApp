from django.http import HttpResponse
from django.shortcuts import render
class HttpResponseMixin(object):
    def render_to_Http_response(self,json_data):
        return HttpResponse(json_data,content_type='application/json')