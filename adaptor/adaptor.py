from adaptor import openstack_parser
import json

def policy2dnf(policy):
    resp = {}
    resp['dnf_policy'] = openstack_parser.policy2dnf(policy)
    return resp

def policy2local(dnf_policy):
    resp = {}
    resp['policy'] = openstack_parser.policy2local(dnf_policy)
    return resp
