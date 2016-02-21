from adaptor import models
from adaptor import serializers
from pyeda.inter import *
import json
import re
import copy

local_tech = 'openstack'          # Constant that defines the cloud technology

def get_tenant(ten):
    tenant = None
    try:
        tenant = models.Tenant.objects.get(name=ten)
    except:
        pass
    return tenant

def get_apf(apf_nm):
    apf = None
    try:
        apf = models.Apf.objects.get(name=apf_nm)
    except:
        pass
    return apf

# Return the Attribute object given a name and if the attribute is or not in the ontology
def get_attribute(attr, att_apf, att_ten, ont):
    attribute = None
    try:
        attribute = models.Attribute.objects.get(apf = att_apf.id, tenant = att_ten.id, ontology = ont, name = attr)
    except:
        try:
            attribute = models.Attribute.objects.get(apf = None, tenant = att_ten.id, ontology = ont, name = attr)
        except:
            try:
                attribute = models.Attribute.objects.get(apf = att_apf.id, tenant = None, ontology = ont, name = attr)
            except:
                try:
                    attribute = models.Attribute.objects.get(apf = None, tenant = None, ontology = ont, name = attr)
                except:
                    # print("  ", attr, att_apf, ten, ont)
                    pass
    return attribute

# Return the Operator object given a name and if the operator is or not in the ontology
def get_operator(op, ont):
    operator = None
    try:
        operator = models.Operator.objects.get(ontology = ont, name = op)
    except:
        pass
    return operator

# Return the Value object given a name and the attribute id
def get_value(val, attr):
    value = None
    try:
        value = models.Value.objects.get(attribute_id = attr.id, name = val)
    except:
        pass
    return value

# Receive a value and return a list of variables
def parse_variables(value, ont):
    vars = []

    if ont:
        var = re.compile('(\$\([^\)]*\))')
        vars = var.findall(value)
    else:
        if local_tech == "openstack":
            var = re.compile('(%\([^\)]*\)s)')
            vars = var.findall(value)
        elif local_tech == "aws":
            var = re.compile('(\$\{[^\}]*\})')
            vars = var.findall(value)
        else:
            print("Error: Cloud technology "+local_tech+" is not supported.")

    return vars

# Receive an attribute (loc/ont) and return its equivalent(s) (ont/loc)
def map_attr(attr, apf, tenant):
    attributes = []
    if attr.ontology:
        attribute_map = models.AttributeMapping.objects.filter(apf_attribute = attr.id).all()
        for a_map in attribute_map:
            if (a_map.local_attribute.tenant is None or a_map.local_attribute.tenant == tenant) and (a_map.local_attribute.apf is None or a_map.local_attribute.apf  == apf):
                attributes.append(a_map.local_attribute)
    else:
        attribute_map = models.AttributeMapping.objects.filter(local_attribute = attr.id).all()
        for a_map in attribute_map:
            if (a_map.apf_attribute.tenant is None or a_map.apf_attribute.tenant == tenant) and (a_map.apf_attribute.apf is None or a_map.apf_attribute.apf  == apf):
                attributes.append(a_map.apf_attribute)
    return attributes

# Receive an operator (loc/ont) and return its equivalent(s) (ont/loc)
def map_op(op, apf, tenant):
    operators = []
    if op.ontology:
        operator_map = models.OperatorMapping.objects.filter(apf_operator = op.id).all()
        for o_map in operator_map:
            operators.append(o_map.local_operator)
    else:
        operator_map = models.OperatorMapping.objects.filter(local_operator = op.id).all()
        for o_map in operator_map:
            operators.append(o_map.apf_operator)
    return operators

# Receive a value (loc/ont) and return its equivalent(s) (ont/loc)
def map_val(val, apf, tenant):
    values = []
    if val.attribute.enumerated:
        if val.attribute.ontology:
            value_map = models.ValueMapping.objects.filter(apf_value = val.id).all()
            for v_map in value_map:
                if (v_map.local_value.attribute.apf == apf or v_map.local_value.attribute.apf is None) and (v_map.local_value.attribute.tenant == tenant or v_map.local_value.attribute.tenant is None):
                    values.append(v_map.local_value)
        else:
            value_map = models.ValueMapping.objects.filter(local_value = val.id).all()
            for v_map in value_map:
                if (v_map.apf_value.attribute.apf == apf or v_map.apf_value.attribute.apf is None) and (v_map.apf_value.attribute.tenant == tenant or v_map.apf_value.attribute.tenant is None):
                    values.append(v_map.apf_value)

    else: # Infinite values
        vars = parse_variables(val.name, val.attribute.ontology)   # Find the variables inside the value name (String)
        for v in vars:                                             # For each variable...
            v_val = get_value(v, val.attribute)                    # ... find the Value object
            if v_val:
                if v_val.attribute.ontology:
                    value_map = models.ValueMapping.objects.filter(apf_value = v_val.id).all()
                    for v_map in value_map:
                        if (v_map.local_value.attribute.apf == apf or v_map.local_value.attribute.apf is None) and (v_map.local_value.attribute.tenant == tenant or v_map.local_value.attribute.tenant is None):
                            if v_map.local_value.attribute.enumerated:
                                values.append(v_map.local_value)
                            else:
                                new_val = copy.deepcopy(v_map.local_value)
                                new_val.name = val.name.replace(v, v_map.local_value.name)
                                values.append(new_val)

                else:
                    value_map = models.ValueMapping.objects.filter(local_value = v_val.id).all()
                    for v_map in value_map:
                        if (v_map.apf_value.attribute.apf == apf or v_map.apf_value.attribute.apf is None) and (v_map.apf_value.attribute.tenant == tenant or v_map.apf_value.attribute.tenant is None):
                            if v_map.apf_value.attribute.enumerated:
                                values.append(v_map.apf_value)
                            else:
                                new_val = copy.deepcopy(v_map.apf_value)
                                new_val.name = val.name.replace(v, v_map.apf_value.name)
                                values.append(new_val)
    return values

def obj2str(o):
    txt = None
    txt = o.name
    return txt

def list2str(l):
    txt = None
    if type(l) is list:
        txt = "["
        for v in l:
            txt += to_str(v)
            txt += ", "
        txt += "]"
    return txt

def map2str(m):
    txt = None
    if type(m) is dict:
        txt = "{"
        for k, v in m.items():
            txt += to_str(k)
            txt += ": "
            txt += to_str(v)
            txt += ", "
        txt += "}"
    return txt

def to_str(v):
    txt = ""
    if type(v) is models.Value or type(v) is models.Attribute or type(v) is models.Operator:
        txt += obj2str(v)
    elif type(v) is str:
        txt += v
    elif type(v) is int:
        txt += str(v)
    elif type(v) is list:
        txt += list2str(v)
    elif type(v) is dict:
        txt += map2str(v)
    else:
        txt += "--Unmapped--"
    return txt

# Check if a value contains a local variable.
def is_local_variable(val):
    ret = False
    unknown_tech = False

    if local_tech == "openstack":
        var = re.compile('%\(([^\)]*)\)s')
    elif local_tech == "aws":
        var = re.compile('\$\{([^\}]*)\}')
    else:
        print("Error: Cloud technology "+local_tech+" is not supported.")
        unknown_tech = True

    if not unknown_tech:
        vars = var.findall(val)
        if len(vars) > 0:
            ret = True

    return ret

# Split a list of values in two lists, the first containing the constant values, and the other containing the values with variables.
def split_values(values):
    unknown_tech = False

    if local_tech == "openstack":
        var = re.compile('%\(([^\)]*)\)s')
    elif local_tech == "aws":
        var = re.compile('\$\{([^\}]*)\}')
    else:
        print("Error: Cloud technology "+local_tech+" is not supported.")
        unknown_tech = True

    consts = []
    vars = []

    if not unknown_tech:
        # Find variables in vals and keep them separated
        for val in values:
            if var.findall(val):
                vars.append(val)
            else:
                consts.append(val)

    return consts, vars

def map_val_enum(val, mapped_vals, apf, tenant):
    # Find the mappings for the value (val)
    value_map = models.ValueMapping.objects.filter(apf_value = val.id).all()  # Get all mappings for this Ont value

    # Append mapped values to a temporary dictionary for the mapped attribute
    tmp_vals = {}
    for v_map in value_map:
        v_att = v_map.local_value.attribute
        v_val = v_map.local_value
        if (v_att.apf == apf or v_att.apf is None) and (v_att.tenant == tenant or v_att.tenant is None):
            if v_att not in tmp_vals.keys():
                tmp_vals[v_att] = []
            tmp_vals[v_att].append(v_val)

    # Combine the list of candidate values with the previous list for the attribute
    for k, vs in tmp_vals.items():
        if k not in mapped_vals.keys():
            mapped_vals[k] = vs
        else:
            if v_att.enumerated:
                mapped_vals[k] = list(set(mapped_vals[k]) & set(vs)) # Intersection for enumerated
            else:
                mapped_vals[k] = list(set(mapped_vals[k]) | set(vs)) # Union for infinite

    return mapped_vals

# Map conditions with attributes on the ontology onto local conditions
def map_conditions(new_conds, apf, tenant):
    ret = {}
    for op, attvals in new_conds.items():   # List of all atts/vals in the condition per operator
        values = []
        mapped_vals = {}

        for att, vals in attvals.items():
            for val in vals:
                if att.ontology:
                    if att.enumerated:
                        mapped_vals = map_val_enum(val, mapped_vals, apf, tenant)
                    else:
                        vars = parse_variables(val, True)
                        for vr in vars:
                            var = get_value(vr, att)
                            if var:
                                mapped_vals = map_val_enum(var, mapped_vals, apf, tenant)
                                for mv_att, mv_vals in mapped_vals.items():
                                    if not mv_att.enumerated: # If infinite, replace ontology variable with local ones
                                        v_list = []
                                        for mv_val in mv_vals:
                                            v_list.append(val.replace(vr, mv_val.name))
                                        mapped_vals[mv_att] = mv_vals
                            else:
                                print("Error: Variable "+vr+" could not be retrieved.")
                        if len(vars) == 0:              # If no vars were found, the value is a string (infinite)
                            if att not in mapped_vals:
                                mapped_vals[att] = []
                            mapped_vals[att].append(val)        

        for k, vs in mapped_vals.items():
            if k.enumerated:
                num_vals = len(vs)
                candidates = {}
                for v in vs:
                    value_map2 = models.ValueMapping.objects.filter(local_value = v.id).all()
                    match = True
                    for v_map2 in value_map2:
                        v_att2 = v_map2.apf_value.attribute
                        v_val2 = v_map2.apf_value
                        if v_att2 in attvals.keys() and v_val2 in attvals[v_att2]:
                            pass
                        else:
                            match = False
                    if match:
                        if num_vals not in candidates.keys():
                            candidates[num_vals] = []
                        if v not in candidates[num_vals]:
                            candidates[num_vals].append(v)

                        max_val = max(candidates.keys())
                        mapped_vals[k] = candidates[max_val]

        mapped_vals_str = {}

        for k, vs in mapped_vals.items():
            if k.name not in mapped_vals_str.keys():
                mapped_vals_str[k.name] = []
            for v in vs:
                if type(v) is not str:
                    mapped_vals_str[k.name].append(v.name) 
                else:
                    mapped_vals_str[k.name].append(v) 

        if mapped_vals_str:
            ret[op] = mapped_vals_str

    return ret

# Create a condition object to be added in an And Rule
def create_condition(a, o, v):
    cond = {}
    cond['attribute'] = a
    cond['operator'] = o
    cond['value'] = v
    if is_local_variable(v):
        cond['type'] = "v"
    else:
        cond['type'] = "c"   
    cond['description'] = cond['attribute']+cond['operator']+cond['value']
    return cond

# Create new_attr object to be added in condition
def create_new_attribute(name, desc, policy, ct):
    new_att = {}
    new_att['name'] = name
    new_att['description'] = desc
    new_att['cloud_technology'] = ct
    pol = None
    if policy:
        pol = policy.name
    new_att['policy'] = pol
    return new_att

# Create a condition object to be added in an And Rule
def create_new_condition(desc, a, o, v):
    new_c = {}
    new_c['description'] = desc
    new_c['attribute'] = a
    new_c['operator'] = o
    new_c['value'] = v
    return new_c

# Perform policy semantic mapping from Local DNF to Ontology DNF
def semantic2ontology(dnf_policy, ten, apf_nm):
    tenant = get_tenant(ten)
    if not tenant:
        print("Error: Tenant "+ten+" not found.")
        return None 

    apf = get_apf(apf_nm)
    if not apf:
        print("Error: APF "+apf_nm+" not found.")
        return None

    local_and_rules = []                      # List of and rules that are cloud specific
    ont_and_rules = []                        # List of and rules on the ontology
    # Iterate through the and rules.
    for ar in dnf_policy['and_rules']:
        new_conds = []                        # Reset NewConditions list
        ar_ontology = True                    # Reset AndRuleInOntology flag

        for c in ar['conditions']:            # Iterate through the conditions.
            cond_ontology = {}                # Reset OnOntology flags

            ######################  Retrieve operator  ###################

            cond_ontology['operator'] = True          # Set initial ontology flag

            lo = get_operator(c['operator'], False)   # Get equivalent op obj

            if not lo :
                # Operator not found
                cond_ontology['operator'] = False     
            else:
                # Operator found: map
                oo_list = map_op(lo, apf, tenant)
                if len(oo_list) != 1:
                    # Multiple operators found: Error
                    cond_ontology['operator'] = False     
                    print("Multiple operators are not accepted.")

            # Set new operator JSON object
            new_op = {}
            if cond_ontology['operator']:
                new_op['name'] = oo_list[0].name
                new_op['description'] = oo_list[0].description
                new_op['cloud_technology'] = None
            else:
                new_op['name'] = c['operator']
                new_op['description'] = None
                new_op['cloud_technology'] = local_tech

            ######################  Retrieve attribute & value  ###################

            cond_ontology['attribute'] = True       # Set initial ontology flags
            cond_ontology['value'] = True
            oa_list = []
            ov_list = []

            la = get_attribute(c['attribute'], apf, tenant, False) # Get equivalent att obj
            if la:
                oa_list = map_attr(la, apf, tenant)                # Attribute found: map
                lv = get_value(c['value'], la)                     # Get equivalent val obj
                if lv:
                    ov_list = map_val(lv, apf, tenant)             # Value found: map

            ###################### Create Mapped Conditions ########################

            if oa_list and ov_list:                              # Attribute found - Value found
                for ov in ov_list:
                    new_att = {}
                    if ov.attribute in oa_list:                  # Attribute corresponds to value
                        new_value = ov.name
                        new_att = create_new_attribute(ov.attribute.name, ov.attribute.description, ov.attribute.apf, None)

                    else:                                        # Attribute doesn't correspond to value
                        cond_ontology['value'] = False           # This is odd. If the value corresponded to the local attribute
                        new_value = c['value']                   # its mapped equivalent should be mapped to an ontology attribute
                                                                 # Solution: Set Attribute and Value as cloud specific, and log warning.
                        cond_ontology['attribute'] = False
                        new_att = create_new_attribute(c['attribute'], None, la.apf, local_tech)

                        print("Warning: Ontology equivalents for the local attribute/value pair does not match!", to_str(ov.attribute), to_str(oa_list))
                        
                    new_c = create_new_condition(c['description'], new_att, new_op, new_value)
                    if new_c not in new_conds:
                        new_conds.append(new_c)

            elif oa_list and not ov_list:                           # Attribute found - Value not found
                for oa in oa_list:
                    new_value = c['value']
                    vars = parse_variables(new_value, False)
                    if not oa.enumerated and not vars:              # If the attribute is infinite and there are no variables, it can be mapped to ontology
                        new_att = create_new_attribute(oa.name, oa.description, oa.apf, None)
                        new_c = create_new_condition(c['description'], new_att, new_op, new_value)
                        if new_c not in new_conds:
                            new_conds.append(new_c)
                    else:                                           # Otherwise, if the attribute is enumerated or finite with variables, the local will be kept
                        cond_ontology['value'] = False
                        new_att = create_new_attribute(c['attribute'], None, la.apf, local_tech)
                        new_c = create_new_condition(c['description'], new_att, new_op, new_value)
                        if new_c not in new_conds:
                            new_conds.append(new_c)

            else:                                                       # Attribute and value not found
                cond_ontology['value'] = False
                new_value = c['value']

                cond_ontology['attribute'] = False
                new_att = create_new_attribute(c['attribute'], None, None, local_tech)
                new_c = create_new_condition(c['description'], new_att, new_op, new_value)
                if new_c not in new_conds:
                    new_conds.append(new_c)

            # If attribute, operator or value are not on the ontology, the and rule is also not on
            if not cond_ontology['operator'] or not cond_ontology['attribute'] or not cond_ontology['value']:
                 ar_ontology = False

        ar['conditions'] = new_conds             # Copy conditions to And Rule
        new_ar = copy.deepcopy(ar)               # Create new object (copy)

        if ar_ontology:                          # Attach new object to list
            if new_ar not in ont_and_rules:
                ont_and_rules.append(new_ar)
        else:
            if new_ar not in local_and_rules:
                local_and_rules.append(new_ar)

    print(len(ont_and_rules))
    print(len(local_and_rules))

    ret = {}
    ret['and_rules'] = ont_and_rules + local_and_rules

    return ret

# Perform policy semantic mapping from Ontology DNF to Local DNF
def semantic2local(policy, ten, apf_nm):
    tenant = get_tenant(ten)
    if not tenant:
        print("Error: Tenant "+ten+" not found.")
        return None 

    apf = get_apf(apf_nm)
    if not apf:
        print("Error: APF "+apf_nm+" not found.")
        return None

    ars = []
    for ar in policy['and_rules']:
        unknown_tech = False                # If this flag is true, the AR will be jumped
        new_conds_ont = {}
        new_conds_local = {}
        for c in ar['conditions']:

            ##################### Operator Mapping ##################
            lo = None

            if c['operator']['cloud_technology'] is None:
                oo = get_operator(c['operator']['name'], True)
                if oo:
                    lo_list = map_op(oo, apf, tenant)
                    if len(lo_list) == 1:
                        lo = lo_list[0].name
                    else:
                        print("Error: Operator "+c['operator']['name']+" could not be mapped to "+local_tech+".")
                else:
                    print("Error: Operator "+c['operator']['name']+" details could not be retrieved.")

            elif  c['operator']['cloud_technology'] == local_tech:
                lo = c['operator']['name']

            else:
                print("Operator technology "+c['operator']['cloud_technology']+" is unknown - AR will be discarded.")

            ##################### Attribute & Value Details ##################

            if lo:
                if  c['attribute']['cloud_technology'] is None:
                    oa = get_attribute(c['attribute']['name'], apf, tenant, True)
                    if oa:
                        if oa.enumerated:                                               # Enumerated Values
                            ov = get_value(c['value'], oa)
                            if ov:
                                if lo not in new_conds_ont.keys():
                                    new_conds_ont[lo] = {}
                                if oa not in new_conds_ont[lo].keys():
                                    new_conds_ont[lo][oa] = []
                                if ov not in new_conds_ont[lo][oa]:
                                    new_conds_ont[lo][oa].append(ov)

                            else:
                                print("Error: Value "+c['value']+" details could not be retrieved.")
                        else:                                                            # Infinite Values
                            if lo not in new_conds_ont.keys():
                                new_conds_ont[lo] = {}
                            if oa not in new_conds_ont[lo].keys():
                                new_conds_ont[lo][oa] = []
                            if c['value'] not in new_conds_ont[lo][oa]:
                                new_conds_ont[lo][oa].append(c['value'])

                    else:
                        print("Error: Attribute "+c['attribute']['name']+" details could not be retrieved.")

                elif c['attribute']['cloud_technology'] == local_tech:
                    if lo not in new_conds_local.keys():
                        new_conds_local[lo] = {}
                    if c['attribute']['name'] not in new_conds_local[lo].keys():
                        new_conds_local[lo][c['attribute']['name']] = []
                    if c['value'] not in new_conds_local[lo][c['attribute']['name']]:
                        new_conds_local[lo][c['attribute']['name']].append(c['value'])

                else:
                    print("AR will be discarded! Attribute technology is unknown:", c['attribute']['cloud_technology'])
                    unknown_tech = True

        if not unknown_tech:

            ##################### Attribute & Value Mapping ##################
    
            new_conds_ont = map_conditions(new_conds_ont, apf, tenant)

            ##################### Attribute & Value Merge ##################

            new_conds = new_conds_ont                    # Start with enumerated atts

            for op, ar_attvals in new_conds_local.items():      # Add local atts
                for k,v in ar_attvals.items():
                    if op not in new_conds:
                        new_conds[op] = {}
                    if k not in new_conds[op]:
                        new_conds[op][k] = []
                    new_conds[op][k] = new_conds[op][k] + v

            ################## Create condition and add them to ars ##################

            cs_or = []
            cs_and = []

            for op, ar_attvals in new_conds.items():

                for k,v in ar_attvals.items():
                    if len(v) > 1:
                        consts, vars = split_values(v)
                        for const in consts:
                            new_c = create_condition(k, op, const)
                            if new_c not in cs_or:
                                cs_or.append(new_c)
                        for var in vars:
                            new_c = create_condition(k, op, var)
                            if new_c not in cs_and:
                                cs_and.append(new_c)
                    else:
                        for val in v:
                            new_c = create_condition(k, op, val)
                            if new_c not in cs_and:
                                cs_and.append(new_c)

            if cs_or:
                for cso in cs_or:
                    ar_tmp = copy.copy(ar)
                    cs_tmp = copy.copy(cs_and)
                    if cso not in cs_tmp:
                        cs_tmp.append(cso)
                    ar_tmp['conditions'] = cs_tmp
                    if ar_tmp not in ars:
                        ars.append(ar_tmp)

            elif cs_and:
                ar['conditions'] = cs_and
                if ar not in ars:
                    ars.append(ar)

    ret = {}
    ret['and_rules'] = ars

    return ret
