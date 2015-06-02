#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adaptor import adaptor

# Create your views here.
class AdaptorDnfView(APIView):
    def post(self, request, *args, **kwargs):
        resp = {}
        if (not "format" in request.data or not "policy" in request.data):
            resp['detail'] = "Missing argument"
            return Response(resp, status=412)
        elif (request.data["format"] == "openstack"):
            resp = adaptor.policy2dnf(request.data["policy"])
            return Response(resp)
        else:
            resp['detail'] = "Policy Format not Supported."
            return Response(resp, status=415)

class AdaptorLocalView(APIView):
    def post(self, request, *args, **kwargs):
        resp = adaptor.policy2local(request.data)
        return Response(resp)
