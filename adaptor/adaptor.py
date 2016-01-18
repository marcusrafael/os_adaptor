from adaptor import openstack_parser
from adaptor import semantic_parser
import json

def policy2dnf(policy):
    resp = {}
    dnfpol = openstack_parser.policy2dnf(policy)
    resp['dnf_policy'] = semantic_parser.semantic2ontology(dnfpol)
    return resp

def policy2local(dnf_policy):
    resp = {}
    locpol = semantic_parser.semantic2local(dnf_policy)
    resp['policy'] = openstack_parser.policy2local(locpol)
    return resp
