"""os_adaptor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from adaptor import views, models

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ('id', 'name', 'description')

class ApfSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apf
        fields = ('id', 'name', 'description')

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute
        fields = ('id', 'tenant', 'apf', 'ontology', 'enumerated', 'name', 'description')

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operator
        fields = ('id', 'tenant', 'apf', 'ontology', 'name', 'description')

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Value
        fields = ('id', 'attribute', 'name', 'description')

class HierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hierarchy
        fields = ('id', 'parent', 'child')

class AttributeMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeMapping
        fields = ('id', 'local_attribute', 'apf_attribute')

class OperatorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OperatorMapping
        fields = ('id', 'local_operator', 'apf_operator')

class ValueMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ValueMapping
        fields = ('id', 'local_value', 'apf_value')

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

router = routers.DefaultRouter()
router.register(r'tenant', views.TenantViewSet)
router.register(r'apf', views.ApfViewSet)
router.register(r'attribute', views.AttributeViewSet)
router.register(r'operator', views.OperatorViewSet)
router.register(r'value', views.ValueViewSet)
router.register(r'hierarchy', views.HierarchyViewSet)
router.register(r'attribute_mapping', views.AttributeMappingViewSet)
router.register(r'operator_mapping', views.OperatorMappingViewSet)
router.register(r'value_mapping', views.ValueMappingViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
#    url(r'^', include(router.urls)),
    url(r'^policy2dnf/', views.AdaptorDnfView.as_view(), name='my_rest_view'),
    url(r'^policy2local/', views.AdaptorLocalView.as_view(), name='my_rest_view'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),
#]
