from apps.adaptor import openstack_parser
from apps.adaptor import semantic_parser
import json

def policy2dnf(policy, tenant, apf):
    resp = {}
    dnfpol = openstack_parser.policy2dnf(policy)
    if dnfpol:
        ontpol = semantic_parser.semantic2ontology(dnfpol, tenant, apf)
    if ontpol:
        resp['dnf_policy'] = ontpol

    # resp['dnf_policy'] = dnfpol

    return resp

def policy2local(dnf_policy, tenant, apf):
    resp = {}
    locpol = semantic_parser.semantic2local(dnf_policy, tenant, apf)
    if (locpol):
        parsedpol = openstack_parser.policy2local(locpol)
    if (parsedpol):
    	resp['policy'] = parsedpol

    # resp['policy'] = locpol

    return resp
