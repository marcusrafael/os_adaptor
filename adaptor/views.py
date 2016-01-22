#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adaptor import adaptor
from rest_framework import viewsets
from adaptor import models
from adaptor.serializers import TenantSerializer, ApfSerializer, AttributeSerializer \
    , OperatorSerializer, ValueSerializer, HierarchySerializer, AttributeMappingSerializer \
    , OperatorMappingSerializer, ValueMappingSerializer

class TenantViewSet(viewsets.ModelViewSet):
    queryset = models.Tenant.objects.all()
    serializer_class = TenantSerializer

class ApfViewSet(viewsets.ModelViewSet):
    queryset = models.Apf.objects.all()
    serializer_class = ApfSerializer

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = models.Attribute.objects.all()
    serializer_class = AttributeSerializer

class OperatorViewSet(viewsets.ModelViewSet):
    queryset = models.Operator.objects.all()
    serializer_class = OperatorSerializer

class ValueViewSet(viewsets.ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = ValueSerializer

class HierarchyViewSet(viewsets.ModelViewSet):
    queryset = models.Hierarchy.objects.all()
    serializer_class = HierarchySerializer

class AttributeMappingViewSet(viewsets.ModelViewSet):
    queryset = models.AttributeMapping.objects.all()
    serializer_class = AttributeMappingSerializer

class OperatorMappingViewSet(viewsets.ModelViewSet):
    queryset = models.OperatorMapping.objects.all()
    serializer_class = OperatorMappingSerializer

class ValueMappingViewSet(viewsets.ModelViewSet):
    queryset = models.ValueMapping.objects.all()
    serializer_class = ValueMappingSerializer

# Create your views here.
class AdaptorDnfView(APIView):
    def post(self, request, *args, **kwargs):
        resp = {}
        if (not "format" in request.data or not "policy" in request.data or not "tenant" in request.data or not "apf" in request.data):
            resp['detail'] = "Missing argument"
            return Response(resp, status=412)
        elif (request.data["format"] == "openstack"):
            resp = adaptor.policy2dnf(request.data["policy"], request.data["tenant"], request.data["apf"])
            return Response(resp)
        else:
            resp['detail'] = "Policy Format not Supported."
            return Response(resp, status=415)

class AdaptorLocalView(APIView):
    def post(self, request, *args, **kwargs):
        resp = {}
        if (not "format" in request.data or not "dnf_policy" in request.data or not "tenant" in request.data or not "apf" in request.data):
            resp['detail'] = "Missing argument"
            return Response(resp, status=412)
        elif (request.data["format"] == "openstack"):
            resp = adaptor.policy2local(request.data["dnf_policy"], request.data["tenant"], request.data["apf"])
            return Response(resp)
        else:
            resp['detail'] = "Policy Format not Supported."
            return Response(resp, status=415)
        return Response(resp)
