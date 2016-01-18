from django.db import models

# Create your models here.

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Apf(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Attribute(models.Model):
    tenant = models.ForeignKey(Tenant, null=True)
    apf = models.ForeignKey(Apf, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    ontology = models.BooleanField(default=False)
    enumerated = models.BooleanField(default=False)

class Operator(models.Model):
    tenant = models.ForeignKey(Tenant, null=True)
    apf = models.ForeignKey(Apf, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    ontology = models.BooleanField(default=False)

class Value(models.Model):
    attribute = models.ForeignKey(Attribute)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Hierarchy(models.Model):
    parent = models.ForeignKey(Value, related_name='parent')
    child = models.ForeignKey(Value, related_name='child')

class AttributeMapping(models.Model):
    local_attribute = models.ForeignKey(Attribute, related_name='local_attribute')
    apf_attribute = models.ForeignKey(Attribute, related_name='apf_attribute')

class OperatorMapping(models.Model):
    local_operator = models.ForeignKey(Operator, related_name='local_operator')
    apf_operator = models.ForeignKey(Operator, related_name='apf_operator')

class ValueMapping(models.Model):
    local_value = models.ForeignKey(Value, related_name='local_value')
    apf_value = models.ForeignKey(Value, related_name='apf_value')