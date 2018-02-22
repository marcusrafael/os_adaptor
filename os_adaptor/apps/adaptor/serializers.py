from rest_framework import serializers
from apps.adaptor import models

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tenant
        fields = ('id', 'name', 'description')

class ApfSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apf
        fields = ('id', 'name', 'description')

class AttributeSerializer(serializers.ModelSerializer):
   # tenant = serializers.PrimaryKeyRelatedField(null=True, read_only=True, allow_null=True) 
   # apf = serializers.PrimaryKeyRelatedField(null=True, read_only=True, allow_null=True) 
    class Meta:
        model = models.Attribute
        fields = ('id', 'tenant', 'apf', 'ontology', 'enumerated', 'name', 'description')

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operator
        fields = ('id', 'ontology', 'name', 'description')

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
