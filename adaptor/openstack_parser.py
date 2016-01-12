from adaptor import models
from adaptor import serializers
from pyeda.inter import *
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

def semantic2ontology(dnf_policy):
    ret = dnf_policy
    local_and_rules = []
    ont_and_rules = []
    cond_ontology = {}
    ar_ontology = True
    # Iterate through the and rules.
    for ar in ret['and_rules']:
        new_conds = []
#        print(json.dumps(ar))
        print(ar['description'])
        ar_ontology = True
        # Iterate through the conditions.
        for c in ar['conditions']:
#            print(c['description'], end=""),
            cond_ontology['attribute'] = True
            cond_ontology['operator'] = True
            cond_ontology['value'] = True

            # Retrieve attribute, operator and value
            lo = get_operator(c['operator'], False)   # Get equivalent op obj
            la = get_attribute(c['attribute'], False) # Get equivalent att obj
            lv = None

            if not lo :
                cond_ontology['operator'] = False     # Operator not found

            if not la :
                cond_ontology['attribute'] = False    # Attribute not found
            else:
                lv = get_value(c['value'], la)        # Get equivalent val obj

            if not lv:
                cond_ontology['value'] = False        # Values not found in ont

            # All found!
            if cond_ontology['operator'] and cond_ontology['attribute'] and cond_ontology['value']:
                oo_list = map_op(lo)
                if len(oo_list) != 1:
                    print("Zero or multiple operators are not accepted.")
                else:
                    oa_list = map_attr(la)
                    ov_list = map_val(lv)
                    for ov in ov_list:
                        if ov.attribute in oa_list:
                            new_c = {}
                            new_c['description'] = c['description']
                            new_c['type'] = c['type']
#                            print("   ", ov.name)
                            new_c['value'] = ov.name
#                            print("   ", oo_list[0].name)
                            new_c['operator'] = oo_list[0].name
#                            print("   ", ov.attribute.name)
                            new_c['attribute'] = ov.attribute.name
                            new_conds.append(new_c)
#                            print(json.dumps(new_c))
                        else:
                            print("Value not accepted for these attributes")
            else:
                ar_ontology = False
                
        # AR
        if ar_ontology:
            ar['conditions'] = new_conds
            ont_and_rules.append(ar)
        else:
            local_and_rules.append(ar)

    print(json.dumps(ont_and_rules, indent=2))
#    print(json.dumps(local_and_rules, indent=2))
    print(len(ont_and_rules))
    print(len(local_and_rules))

#---
#def expand_and_rule_without_hierarchy(and_rule):
#    and_rules = []
#    and_rule_serializer = serializers.And_ruleSerializer(and_rule)
#    andr = copy.copy(and_rule_serializer.data)
#    conditions = []
#    for cond in and_rule.conditions.all():     # Check all Conditions
#        cond_serializer = serializers.ConditionSerializer(cond)
#        conditions.append(cond_serializer.data)
#    andr['conditions'] = conditions
#    and_rules.append(andr)
#    return(and_rules)
#---
    return ret

def semantic2local(policy):
    ret = policy
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

