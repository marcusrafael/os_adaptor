from adaptor import models
from adaptor import serializers
from pyeda.inter import *
# from parse import *
import json
import re
import copy

# Return the Attribute object given a name and if the attribute is or not in the ontology
def get_attribute(attr, ont):
    attribute = None
    try:
        attribute = models.Attribute.objects.get(ontology = ont, name = attr)
    except:
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

# Receive an attribute (loc/ont) and return its equivalent(s) (ont/loc)
def map_attr(attr):
    attributes = []
    if attr.ontology:
        attribute_map = models.AttributeMapping.objects.filter(apf_attribute = attr.id).all()
        for a_map in attribute_map:
            attributes.append(a_map.local_attribute)
    else:
        attribute_map = models.AttributeMapping.objects.filter(local_attribute = attr.id).all()
        for a_map in attribute_map:
            attributes.append(a_map.apf_attribute)
    return attributes

# Receive an operator (loc/ont) and return its equivalent(s) (ont/loc)
def map_op(op):
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
def map_val(val):
    values = []
    if val.attribute.ontology:
        value_map = models.ValueMapping.objects.filter(apf_value = val.id).all()
        for v_map in value_map:
            values.append(v_map.local_value)
    else:
        value_map = models.ValueMapping.objects.filter(local_value = val.id).all()
        for v_map in value_map:
            values.append(v_map.apf_value)
    return values

# Receive a value (loc/ont) and return its equivalent(s) (ont/loc)
def map_val2(val, att_list):
    values = []
    if val.attribute.ontology:
        value_map = models.ValueMapping.objects.filter(apf_value = val.id).all()
        mapped_vals = {}                   
        if len(value_map) > 1:
            for v_map in value_map:     # Mappings for one Value
                value_map2 = models.ValueMapping.objects.filter(local_value = v_map.local_value.id).all()
                cnt = len(value_map2)
                if cnt not in mapped_vals:
                    mapped_vals[cnt] = []
                mapped_vals[cnt].append(value_map2)

            for cnt in sorted(mapped_vals.keys(), reverse=True):       # itereate through the mapped vals in descending order
                for mv_list in mapped_vals[cnt]:
                    passed = True
                    for mv in mv_list:
                        if mv.apf_value.attribute not in att_list:    # Verify if the apf attributes are in the original list
                            passed = False
                    if passed:
                        values.append(mv.local_value)               # If all apf_values are in the original list, add it as candidate
                if len(values) > 0:     # If there is any mapped value with this number of local value candidates, don't get lower numbers
                    break
        else:
            for v_map in value_map:
                values.append(v_map.local_value)

    else:
        value_map = models.ValueMapping.objects.filter(local_value = val.id).all()
        for v_map in value_map:
            values.append(v_map.apf_value)
    return values

# Receive a value and return a list of variables
def parse_variables(value, ont):
    vars = []

    if ont:
        var = re.compile('\$\(([^\)]*)\)')
        vars = var.findall(value)
    else:
        var = re.compile('%\(([^\)]*)\)s')
        vars = var.findall(value)

    return vars

# Receive a list of variables, map them in the ontology and replace them with correct syntax
def parse_value(value, ont):
    ret = value

    vars = parse_variables(value, ont)

    for v in vars:
        att = get_attribute(v, ont)
        if att:
            oa_list = map_attr(att)
            if oa_list:
                for oa in oa_list:
                    if ont:
                        ret = ret.replace("$("+v+")", "%("+oa.name+")s")
                    else:
                        ret = ret.replace("%("+v+")s", "$("+oa.name+")")
            else:
                print("Variable "+v+"has no equivalent.")
                ret = None
        else:
            print("Variable "+v+" is not valid.")
            ret = None

    return ret

# Check if a value contains an Openstack variable.
def is_os_variable(val):
    ret = False
    var = re.compile('%\(([^\)]*)\)s')
    vars = var.findall(val)
    if len(vars) > 0:
        ret = True
    return ret

# Split a list of values in two lists, the first containing the constant values, and the other containing the values with variables.
def split_values(values):
    var = re.compile('%\(([^\)]*)\)s')
    # Find variables in vals and keep them separated
    consts = []
    vars = []
    for val in values:
        if var.findall(val):
            vars.append(val)
        else:
            consts.append(val)
    return consts, vars

# Map conditions with attributes on the ontology that accept Enumerated values onto Openstack conditions
def map_enumerated(new_conds):
    ret = new_conds
    for op, attvals in new_conds.items():   # List of all atts/vals in the condition per operator
        ar_attvals = {}
        for att, vals in attvals.items():   # List of Atts and Values of one operator
            loc_attvals = {}
            la_list = map_attr(att)
            for v in vals:                  # Values of one Att
                candidates = map_val2(v, attvals.keys())     # Map the value and get the candidate values that satisfies the attributes from and_rule
                for cd in candidates:
                    if cd.attribute in la_list:              # Filter candidate values of different attributes
                        if cd.attribute.name not in loc_attvals:
                            loc_attvals[cd.attribute.name] = []
                        loc_attvals[cd.attribute.name].append(cd.name)
            for a, v in loc_attvals.items():
                if a not in ar_attvals:
                    ar_attvals[a] = v
                else:
                    ar_attvals[a] = list(set(v) & set(ar_attvals[a]))
        
        ret[op] = ar_attvals

    return ret

# Map conditions with attributes on the ontology that accept Infinite values onto Openstack conditions
def map_infinite(new_conds):
    ret = new_conds
    for op, attvals in new_conds.items():   # List of all atts/vals in the condition per operator
        ar_attvals = {}
        for att, vals in attvals.items():   # List of Atts and Values of one operator
            loc_attvals = {}
            la_list = map_attr(att)

            for la in la_list:
                if la.name not in ar_attvals:
                    ar_attvals[la.name] = [] 
                for v in vals:                  # Values of one Att
                    lv = parse_value(v, True)
                    if lv not in ar_attvals[la.name]:
                        ar_attvals[la.name].append(lv)
        
        ret[op] = ar_attvals

    return ret

# Create a condition object to be added in an And Rule
def create_condition(a, o, v):
    cond = {}
    cond['attribute'] = a
    cond['operator'] = o
    cond['value'] = v
    if is_os_variable(v):
        cond['type'] = "v"
    else:
        cond['type'] = "c"   
    cond['description'] = cond['attribute']+cond['operator']+cond['value']
    return cond

# Perform policy semantic mapping from Openstack DNF to Ontology DNF
def semantic2ontology(dnf_policy):
    local_and_rules = []                      # List of and rules that are cloud specific
    ont_and_rules = []                        # List of and rules on the ontology
    # Iterate through the and rules.
    for ar in dnf_policy['and_rules']:
        new_conds = []                        # Reset NewConditions list
        ar_ontology = True                    # Reset AndRuleInOntology flag

        # print("----")
        # print(ar['description'])

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
                oo_list = map_op(lo)
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
                new_op['cloud_technology'] = 'openstack'

            ######################  Retrieve attribute & value  ###################

            cond_ontology['attribute'] = True       # Set initial ontology flags
            cond_ontology['value'] = True
            oa_list = []
            ov_list = []

            la = get_attribute(c['attribute'], False) # Get equivalent att obj
            if la:
                oa_list = map_attr(la)                # Attribute found: map
                lv = get_value(c['value'], la)        # Get equivalent val obj
                if lv:
                    ov_list = map_val(lv)             # Value found: map

            ###################### Create Mapped Conditions ########################

            if oa_list and ov_list:                              # Attribute found - Value found
                for ov in ov_list:
                    new_att = {}
                    if ov.attribute in oa_list:                  # Attribute corresponds to value
                        new_value = ov.name

                        new_att['name'] = ov.attribute.name
                        new_att['description'] = ov.attribute.description
                        new_att['cloud_technology'] = None
                        if ov.attribute.apf:
                            new_att['policy'] = ov.attribute.apf.name
                        else:
                            new_att['policy'] = None

                    else:                                        # Attribute doesn't correspond to value
                        cond_ontology['value'] = False           # This is odd. If the value corresponded to the local attribute
                        new_value = c['value']                   # its mapped equivalent should be mapped to an ontology attribute
                                                                 # Solution: Set Attribute and Value as cloud specific, and log warning.
                        cond_ontology['attribute'] = False
                        new_att['name'] = c['attribute']
                        new_att['description'] = None
                        new_att['cloud_technology'] = 'openstack'
                        if la.apf:
                            new_att['policy'] = la.apf.name
                        else:
                            new_att['policy'] = None

                        print("Warning: local attribute/value match, but Ontology equivalents doesn't!")
                        
                    # Set condition and add to the list
                    new_c = {}
                    new_c['description'] = c['description']
                    new_c['attribute'] = new_att
                    new_c['operator'] = new_op
                    new_c['value'] = new_value
                    new_conds.append(new_c)

            elif oa_list and not ov_list:                           # Attribute found - Value not found
                new_c = None

                for oa in oa_list:
                    new_value = parse_value(c['value'], False)      # Try to find variables in it, and map them
                    if new_value and not oa.enumerated:             # If value is valid and attribute is not enumerated
                        new_att = {}
                        new_att['cloud_technology'] = None
                        new_att['name'] = oa.name
                        new_att['description'] = oa.description
                        if oa.apf:
                            new_att['policy'] = oa.apf.name
                        else:
                            new_att['policy'] = None

                        # Set condition and add to the list
                        new_c = {}
                        new_c['description'] = c['description']
                        new_c['attribute'] = new_att
                        new_c['operator'] = new_op
                        new_c['value'] = new_value
                        new_conds.append(new_c)

                        # print(c['description'])
                        # print(oa.name)
                        # print(new_c)

                if not new_c:                                        # Error on Variable mapping or Attribute is enumerated (Else)
                    cond_ontology['value'] = False
                    new_value = c['value']
                    new_att = {}
                    new_att['cloud_technology'] = 'openstack'
                    new_att['name'] = c['attribute']
                    new_att['description'] = None
                    if la.apf:
                        new_att['policy'] = la.apf.name
                    else:
                        new_att['policy'] = None

                    # Set condition and add to the list
                    new_c = {}
                    new_c['description'] = c['description']
                    new_c['attribute'] = new_att
                    new_c['operator'] = new_op
                    new_c['value'] = new_value
                    new_conds.append(new_c)

                    # print(c['description'])
                    # print(new_c)

            else:                                                       # Attribute and value not found
                cond_ontology['value'] = False
                new_value = c['value']

                cond_ontology['attribute'] = False
                new_att['name'] = c['attribute']
                new_att['description'] = None
                new_att['cloud_technology'] = 'openstack'
                new_att['policy'] = None

                # Set condition and add to the list
                new_c = {}
                new_c['description'] = c['description']
                new_c['attribute'] = new_att
                new_c['operator'] = new_op
                new_c['value'] = new_value
                new_conds.append(new_c)

            # If attribute, operator or value are not on the ontology, the and rule is also not on
            if not cond_ontology['operator'] or not cond_ontology['attribute'] or not cond_ontology['value']:
                 ar_ontology = False

        # if ar_ontology:
        #     print(json.dumps(new_conds, indent=2))
        #     print(ar['description'])
        #     for c in ar['conditions']:
        #         print("    ", c['description'])

        ar['conditions'] = new_conds             # Copy conditions to And Rule
        new_ar = copy.deepcopy(ar)               # Create new object (copy)

        # if ar_ontology:
        #     print(json.dumps(new_ar, indent=2))

        if ar_ontology:                          # Attach new object to list
            ont_and_rules.append(new_ar)
        else:
            local_and_rules.append(new_ar)

    # print(json.dumps(ont_and_rules, indent=2))
    # # print(json.dumps(local_and_rules, indent=2))
    print(len(ont_and_rules))
    print(len(local_and_rules))

    ret = {}
    ret['and_rules'] = ont_and_rules + local_and_rules

    return ret

# Perform policy semantic mapping from Ontology DNF to Openstack DNF
def semantic2local(policy):
    ars = []
    for ar in policy['and_rules']:
        unknown_tech = False                # If this flag is true, the AR will be jumped
        new_conds_enumerated = {}
        new_conds_infinite = {}
        new_conds_local = {}
        for c in ar['conditions']:

            ##################### Operatot Mapping ##################
            lo = None

            if c['operator']['cloud_technology'] is None:
                oo = get_operator(c['operator']['name'], True)
                if oo:
                    lo_list = map_op(oo)
                    if len(lo_list) == 1:
                        lo = lo_list[0].name
                    else:
                        print("Error: Operator "+c['operator']['name']+" could not be mapped to Openstack.")
                else:
                    print("Error: Operator "+c['operator']['name']+" details could not be retrieved.")

            elif  c['operator']['cloud_technology'] == 'openstack':
                lo = c['operator']['name']

            else:
                print("Operator technology "+c['operator']['cloud_technology']+" is unknown - AR will be discarded.")

            ##################### Attribute & Value Details ##################

            if lo:
                if  c['attribute']['cloud_technology'] is None:
                    oa = get_attribute(c['attribute']['name'], True)
                    if oa:
                        if oa.enumerated:                                               # Enumerated Values
                            ov = get_value(c['value'], oa)
                            if ov:
                                if lo not in new_conds_enumerated.keys():
                                    new_conds_enumerated[lo] = {}
                                if oa not in new_conds_enumerated[lo].keys():
                                    new_conds_enumerated[lo][oa] = []
                                if ov not in new_conds_enumerated[lo][oa]:
                                    new_conds_enumerated[lo][oa].append(ov)

                            else:
                                print("Error: Value "+c['value']+" details could not be retrieved.")
                        else:                                                            # Infinite Values
                            if lo not in new_conds_infinite.keys():
                                new_conds_infinite[lo] = {}
                            if oa not in new_conds_infinite[lo].keys():
                                new_conds_infinite[lo][oa] = []
                            if c['value'] not in new_conds_infinite[lo][oa]:
                                new_conds_infinite[lo][oa].append(c['value'])

                    else:
                        print("Error: Attribute "+c['attribute']['name']+" details could not be retrieved.")

                elif c['attribute']['cloud_technology'] == 'openstack':
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

            new_conds = new_conds_enumerated

            ##################### Attribute & Value Mapping ##################
    
            new_conds_enumerated = map_enumerated(new_conds_enumerated)
            new_conds_infinite = map_infinite(new_conds_infinite)

            ##################### Attribute & Value Merge ##################

            new_conds = new_conds_enumerated                    # Start with enumerated atts

            for op, ar_attvals in new_conds_infinite.items():   # Add infinite atts
                for k,v in ar_attvals.items():
                    if k not in new_conds[op]:
                        new_conds[op][k] = []
                    new_conds[op][k] = new_conds[op][k] + v

            for op, ar_attvals in new_conds_local.items():      # Add local atts
                for k,v in ar_attvals.items():
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
                            cs_or.append(create_condition(k, op, const))
                        for var in vars:
                            cs_and.append(create_condition(k, op, var))
                    else:
                        for val in v:
                            cs_and.append(create_condition(k, op, val))

            cs = copy.deepcopy(cs_and)

            if cs_or:
                for cso in cs_or:
                    cs = cs.append(cso)
                    ar['conditions'] = cs
                    ars.append(ar)

            else:
                ar['conditions'] = cs
                ars.append(ar)

    ret = {}
    ret['and_rules'] = ars

    return ret

# Return the oposite operator
def oposite_operator(operator):
    if operator == "=":
        return "!="
    elif operator == "!=":
        return "="
    elif operator == ">":
        return "<="
    elif operator == "<":
        return ">="
    elif operator == ">=":
        return "<"
    elif operator == "<=":
        return ">"
    else:
        return "not "+operator

# Extract a list of conditions from the policy JSON object
def parse_conds(attr, value, policy, conds, rules):
    # Add the regular conditions (from the values) and create the rules array
    if (':' in attr) and (attr not in rules):  # If it is a policy rule and there is no rule entry...
        rules[attr] = value                    # Add an entry into the rules array for the value
    value = value.replace('not', '')           # Remove all the 'not's from the value
    if(attr != '' and value != ''):            # Ignore empty lines
        values = re.split(" and | or ", value) # Use ' and ' or ' or ' to split the value
        for v in values:                       # Loop for all "rules" in value 
            v = v.strip('(').strip(')')        # Remove the parentheses in the rule
            v = v.replace(' ', '')             # Remove all spaces in the rule
            if v[:5] == 'rule:':               # If the rules refers to another rule...
                newv = policy[v[5:]]           # Replace the "rule" by its reference
                if ':' in attr:                                                    # If it is a police rule...
                    rules[attr] = rules[attr].replace(v, newv)                     # Replace the rule in the rules array
                conds, rules = parse_conds(attr, newv, policy, conds, rules)  # Recursive call with the new "rule" as value 
                                                                                   #     (it can have rules again into the reference)
            else:                                                                  # If the rules don't refer to any other rule...
                at, vl = v.split(':')                                              # Split the "rule" in "attribute":"value"
                entry = {'attribute': at, 'operator':'=', 'value': vl}   # Create a new condition entry
                if entry not in conds:                                             # If the entry is not in the condition list...
                    conds = conds + [entry]                                        # Add it to the list

    # Add service/action conditions to the list of conditions
    if ':' in attr:                             # Ignores lines which are not policy rules (i.e. subject rules)
        left = attr[:attr.find(':')]            # Split attribute by the first colon (:) occurence (service:action)
        right = attr[attr.find(':')+1:]

        entry_l = {'attribute': 'service', 'operator':'=', 'value': left}  # Create a new condition entry for the service
        entry_r = {'attribute': 'action', 'operator':'=', 'value': right}  # Create a new condition entry for the action

        if (entry_l not in conds):     # If the service condition is not in the list...
            conds = conds + [entry_l]  # Add it to the list
        if (entry_r not in conds):     # If the action condition is not in the list...
            conds = conds + [entry_r]  # Add it to the list

    return conds, rules                       # Return the list of conditions and the list of rules

def parse_rules(attr, value, conds, rules):
    left = attr[:attr.find(':')]            # Split attribute by the first colon (:) occurence (service:action)
    right = attr[attr.find(':')+1:]

    value = value.replace(' and ',' & ')
    value = value.replace(' or ',' | ')
    value = value.replace('not ','~')
    value = value.replace('not','~')

    service = -1
    action = -1
    i = 0;
    for c in conds:
        at = c['attribute'].replace('\%','\\\%').replace('\.','\\\.')
        vl = c['value'].replace('\%','\\\%').replace('\.','\\\.')
        value = value.replace(at+':'+vl, 'c'+str(i))
        if c['value'] == left:
            service = i
        if c['value'] == right:
            action = i
        i = i + 1
    if service >= 0 and action >= 0:
        if value == '':
            rules[attr] = 'c'+str(service)+' & '+'c'+str(action)
        else:
            rules[attr] = 'c'+str(service)+' & '+'c'+str(action)+' & ('+value+')'
    else:
        print ("Problem... Didn't find service or action")
        rules[attr] = value

    return rules

def parse(ext_pol):

    conds = []
    rules = {}

    # Read rules and extract the conditions
    # eg.: [{"attr_category": "S", "attr": "role", "op": "=", "value", "admin"}, ...]
    # Also prepares a dictionary of rules
    for attr, value in ext_pol.items():
        conds, rules = parse_conds(attr, value, ext_pol, conds, rules)

    # Convert the dictionary in terms of conditions (C0, C1, ...)
    # eg.: {"admin_required": "C1 OR C2", ...}
    # Add service and action rules
    for attr, value in rules.items():
        rules = parse_rules(attr, value, conds, rules)

    return conds, rules

def to_dnf(conds, rules):
    # Define global variables for each condition as a boolean expression
    gbl = globals()
    for i in range(len(conds)):
        var = "c"+str(i)
        gbl[var] = exprvar(var)

    # Define expression based on subject rules and convert them to DNF
    for rk, rv in rules.items():
        #print(rv)
        #print(type(rv))
        gbl[rk] = eval(rv)
        #print(type(gbl[rk]))
        rules[rk] = gbl[rk].to_dnf()

    return rules

def policy2dnf(policy):

    # DNF JSON object
    dnf_policy = {}
    and_rules = []

    # Parses policy content.
    conds, rules = parse(policy)

    # Tranform rules to DNF
    rules = to_dnf(conds,rules)

    # Create and_rules in an DNF JSON (memory)
    for r in rules.items():

        # Only consider namespaced rules
        if ':' in r[0]:
            r1 = str(r[1]).strip()
            r1 = re.sub(' ', '', r1)

            # Add the conditions
            if "Or(" == r1[0:3]:
                s = r1[3:-1]
                s = s.strip('And') # Remove the And in the beginning of the string
                ands = s.split(",And") # Split using the ,And
                count = 0
                for a in ands:
                    # Construct the conditions
                    cs = a.split(",")
                    conditions = []
                    for c in cs:
                        c = re.sub('[,()c]','',c)
                        not_cond = False                # Start considering not a negation
                        if c[0] == "~":                 # If this is a negation
                            not_cond = True                   # Mark as negation
                            c = re.sub('~','',c)              # Remove the negation symbol (~)
                        if (c != "") and c is not None:
                            c = int(float(c))
                            cd = copy.copy(conds[c])
                            if not_cond:
                                cd['operator'] = oposite_operator(cd['operator'])
                            if cd['value'].find("%(") == 0 and cd['value'].rfind(")s") == len(cd['value']) - 2:
                                cd['type'] = "v"
                            else:
                                cd['type'] = "c"
                            cd['description'] = cd['attribute']+cd['operator']+cd['value']
                            conditions.append(cd)
                    # Create the AND Rule
                    data = {
                             "description": r[0]+":"+str(count),
                             "enabled": True,
                             "conditions": conditions
                           }
                    and_rules.append(data)
                    count = count + 1

            elif "And(" == r1[0:4]:
                s = r1[4:-1]

                # Construct the conditions
                cs = s.split(",")
                conditions = []
                for c in cs:
                    c = re.sub('[,()c]','',c)
                    not_cond = False                # Start considering not a negation
                    if c[0] == "~":                 # If this is a negation
                        not_cond = True                   # Mark as negation
                        c = re.sub('~','',c)              # Remove the negation symbol (~)
                    if (c != "") and c is not None:
                        c = int(float(c))
                        cd = copy.copy(conds[c])
                        if not_cond:
                            cd['operator'] = oposite_operator(cd['operator'])
                        if cd['value'].find("%(") == 0 and cd['value'].rfind(")s") == len(cd['value']) - 2:
                            cd['type'] = "v"
                        else:
                            cd['type'] = "c"
                        cd['description'] = cd['attribute']+cd['operator']+cd['value']
                        conditions.append(cd)
                # Insert the AND Rule
                data = {
                         "description": r[0],
                         "enabled": True,
                         "conditions": conditions
                       }
                and_rules.append(data)

            else:
                print ("OTHER: Error!?")
                conditions = []
                c = r1
                c = c.strip(',').strip('(').strip(')').strip('c')
                print(c)

                not_cond = False                # Start considering not a negation
                if c[0] == "~":                 # If this is a negation
                    not_cond = True                   # Mark as negation
                    c = re.sub('~','',c)              # Remove the negation symbol (~)

                # Construct the conditions
                if (c != "") and c is not None:
                    c = int(float(c))
                    cd = copy.copy(conds[c])
                    if not_cond:
                        cd['operator'] = oposite_operator(cd['operator'])
                    if cd['value'].find("%(") == 0 and cd['value'].rfind(")s") == len(cd['value']) - 2:
                        cd['type'] = "v"
                    else:
                        cd['type'] = "c"
                    cd['description'] = cd['attribute']+cd['operator']+cd['value']
                    conditions.append(cd)

                # Insert the AND Rule for the current policy rule
                data = {
                         "description": r[0],
                         "enabled": True,
                         "conditions": conditions
                       }
                and_rules.append(data)
    dnf_policy['and_rules'] = and_rules
    return dnf_policy

def policy2local(dnf_policy):
    policy = {}
    if 'and_rules' in dnf_policy: # If there is no and_rules, just return an empty policy
        for and_rule in dnf_policy['and_rules']: # For each and_rule
            enabled = True
            if 'enabled' in and_rule:
                enabled = and_rule['enabled']
            if enabled:  # If it is enabled
                service = ""
                action  = ""
                condition = ""
                for cond in and_rule['conditions']:    # Check all Conditions
                    not_cond = ""
                    if 'operator' in cond:
                        if cond['operator'] == "!=":
                            not_cond = "not "
                    if 'attribute' in cond:
                        if cond['attribute'] == "service":    # Retrieve the Service
                            service = cond['value']
                        elif cond['attribute'] == "action":   # Retrieve the Action
                            action = cond['value']
                        else:                              # Retrieve the other Conditions (combining with "and"s)
                            if condition == "":
                                condition = not_cond + cond['attribute'] + ":" + cond['value']
                            else:
                                condition = condition + " and " + not_cond + cond['attribute'] + ":" + cond['value']
                    else:
                        print(cond)

                # Insert the and_rule in the policy
                if service+":"+action in policy:           # Set the policy entry. If already exists, combine with "or"s
                    if condition.find("and") == -1:
                        policy[service+":"+action] = policy[service+":"+action] + " or " + condition
                    else:
                        policy[service+":"+action] = policy[service+":"+action] + " or (" + condition + ")"
                else:
                    if condition.find("and") == -1:        # Includes the case: condition == ""
                        policy[service+":"+action] = condition
                    else:
                        policy[service+":"+action] = "(" + condition + ")"
    return policy