from adaptor import openstack_parser
import json

def policy2dnf(policy):
    resp = {}
    resp['dnf_policy'] = openstack_parser.create_and_rules_and_conditions(policy)
    return resp

def policy2local(data):
    resp = data
    return resp
