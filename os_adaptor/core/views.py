from apps.adaptor import adaptor
from apps.adaptor import models
from apps.adaptor import serializers
from rest_framework import response
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets


class TenantViewSet(viewsets.ModelViewSet):
    queryset = models.Tenant.objects.all()
    serializer_class = serializers.TenantSerializer

class ApfViewSet(viewsets.ModelViewSet):
    queryset = models.Apf.objects.all()
    serializer_class = serializers.ApfSerializer

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = models.Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer

class OperatorViewSet(viewsets.ModelViewSet):
    queryset = models.Operator.objects.all()
    serializer_class = serializers.OperatorSerializer

class ValueViewSet(viewsets.ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = serializers.ValueSerializer

class HierarchyViewSet(viewsets.ModelViewSet):
    queryset = models.Hierarchy.objects.all()
    serializer_class = serializers.HierarchySerializer

class AttributeMappingViewSet(viewsets.ModelViewSet):
    queryset = models.AttributeMapping.objects.all()
    serializer_class = serializers.AttributeMappingSerializer

class OperatorMappingViewSet(viewsets.ModelViewSet):
    queryset = models.OperatorMapping.objects.all()
    serializer_class = serializers.OperatorMappingSerializer

class ValueMappingViewSet(viewsets.ModelViewSet):
    queryset = models.ValueMapping.objects.all()
    serializer_class = serializers.ValueMappingSerializer

# Create your views here.
class AdaptorDnfView(views.APIView):
    def post(self, request, *args, **kwargs):
        resp = {}
        if (not "format" in request.data or not "policy" in request.data or not "tenant" in request.data or not "apf" in request.data):
            resp['detail'] = "Missing argument"
            return response.Response(resp, status=412)
        elif (request.data["format"] == "openstack"):
            resp = adaptor.policy2dnf(request.data["policy"], request.data["tenant"], request.data["apf"])
            return Response(resp)
        else:
            resp['detail'] = "Policy Format not Supported."
            return response.Response(resp, status=415)

class AdaptorLocalView(views.APIView):
    def post(self, request, *args, **kwargs):
        resp = {}
        if (not "format" in request.data or not "dnf_policy" in request.data or not "tenant" in request.data or not "apf" in request.data):
            resp['detail'] = "Missing argument"
            return response.Response(resp, status=412)
        elif (request.data["format"] == "openstack"):
            resp = adaptor.policy2local(request.data["dnf_policy"], request.data["tenant"], request.data["apf"])
            return response.Response(resp)
        else:
            resp['detail'] = "Policy Format not Supported."
            return response.Response(resp, status=415)
        return response.Response(resp)
