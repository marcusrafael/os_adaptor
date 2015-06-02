from pyeda.inter import *
import json
import re

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
                entry = {'attr': at, 'op':'=', 'value': vl}   # Create a new condition entry
                if entry not in conds:                                             # If the entry is not in the condition list...
                    conds = conds + [entry]                                        # Add it to the list

    # Add service/action conditions to the list of conditions
    if ':' in attr:                             # Ignores lines which are not policy rules (i.e. subject rules)
        left = attr[:attr.find(':')]            # Split attribute by the first colon (:) occurence (service:action)
        right = attr[attr.find(':')+1:]

        entry_l = {'attr': 'service', 'op':'=', 'value': left}  # Create a new condition entry for the service
        entry_r = {'attr': 'action', 'op':'=', 'value': right}  # Create a new condition entry for the action

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
        at = c['attr'].replace('\%','\\\%').replace('\.','\\\.')
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
        gbl[rk] = eval(rv)
        rules[rk] = gbl[rk].to_dnf()

    return rules

def create_and_rules_and_conditions(external_policy):

    # DNF JSON object
    dnf_policy = {}
    and_rules = []

    # Parses external_policy content.
    conds, rules = parse(external_policy)

    # Tranform rules to DNF
    rules = to_dnf(conds,rules)

    # Create and_rules in an DNF JSON (memory)
    for r in rules.items():

        # Only consider policy rules
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
                    cs = s.split(",")
                    conditions = []
                    for c in cs:
                        c = re.sub('[,()c]','',c)
                        if (c != "") and c is not None:
                            c = int(float(c))
                            cd = conds[c]
                            conditions.append(cd)
                    # Create the AND Rule
                    data = {
                             #"policy": instance,
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
                    if (c != "") and c is not None:
                        c = int(float(c))
                        cd = conds[c]
                        conditions.append(cd)
                # Insert the AND Rule
                data = {
                         #"policy": instance,
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

                # Construct the conditions
                if (c != "") and c is not None:
                    c = int(float(c))
                    cd = conds[c]
                    conditions.append(cd)

                # Insert the AND Rule for the current policy rule
                data = {
                         #"policy": instance,
                         "description": r[0],
                         "enabled": True,
                         "conditions": conditions
                       }
                and_rules.append(data)
    dnf_policy['and_rules'] = and_rules
    return dnf_policy

def export_openstack_policy(policy_id, filters):
    policy = {}
    and_rules = models.And_rule.objects.filter(policy = policy_id).all()
    for and_rule in and_rules: # For each and_rule
        if and_rule.enabled:  # If it is enabled
            service = ""
            action  = ""
            condition = ""
            # TODO: Check if Operator is = (equals). If it is != (not equals), append not in front of value.
            for cond in and_rule.conditions.all():     # Check all Conditions
                if cond.attribute == "service":        # Retrieve the Service
                    service = cond.value         
                elif cond.attribute == "action":       # Retrieve the Action
                    action = cond.value
                else:                                  # Retrieve the other Conditions (combining with "and"s)
                    if condition == "":
                        condition = cond.attribute + ":" + cond.value
                    else:
                        condition = condition + " and " + cond.attribute + ":" + cond.value

            # Only imput policy if service & action matches with filters parameter
            # Cases:
            # 1) service:action
            # 2) service:None
            # 3) None:action
            # 4) None:None (no filter)
            filter = False
            if (filters['service'] == service or filters['service'] is None) \
               and (filters['action'] == action or filters['action'] is None):
                filter = True

            # If filter matches, insert the policy. Otherwise, go to the other policy entry
            if filter:
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

# This function returns all actions that are allowed when the attributes from
# request matches and there is no other required from the same type.
# Other attributes are left as conditions
def actions(queryset, attributes):
    # Cases:

    # 1) condition = "role:match" ==> Granted (G)                               Role_match     and not Other_role and not Other_cond
    # 2) condition = "" ==> Granted (G)                                         not Role_match and not Other_role and not Other_cond

    # 3) condition = "role:match and xxxx" ==> Granted with condition (C)       Role_match     and not Other_role and     Other_cond
    # 4) condition = "..." ==> Granted with condition (C)                       not Role_match and not Other_role and     Other_cond

    # 5) condition = "role:not_match" ==> Not Granted (N)                       not Role_match and     Other_role and not Other_cond     
    # 6) condition = "role:not_match and ..." ==> Not Granted (N)               not Role_match and     Other_role and     Other_cond

    # if Granted or ... ==> Granted
    # elif Granted_with_cond or ... ==> Granted_with_cond
    # else Not Granted

    attributes = json.loads(attributes)    #{"role": ["admin"], "attr2": [--list--]}

    resp = {}
    access = {}
    for and_rule in queryset:
        if and_rule.enabled:

            attr_match = False
            wrong_attr = False
            other_cond = False

            service = ""
            action = ""
            condition = ""

            # Find out the Case
            for cond in and_rule.conditions.all():
                if cond.attribute == "service":
                    service = cond.value
                elif cond.attribute == "action":
                    action = cond.value
                elif cond.attribute in attributes:
                    if cond.type == "c":
                        if type(attributes[cond.attribute]) is list:
                            match = (cond.value in attributes[cond.attribute])
                        else: #string
                            match = (cond.value == attributes[cond.attribute])
                        if match:
                            attr_match = True
                        else:
                            wrong_attr = True
                    else:
                        other_cond = True
                        attr_match = True
                        if condition == "":
                            condition = cond.attribute + ":" + cond.value
                        else:
                            condition = condition + " and " + cond.attribute + ":" + cond.value
                else:
                    other_cond = True
                    if condition == "":
                        condition = cond.attribute + ":" + cond.value
                    else:
                       condition = condition + " and " + cond.attribute + ":" + cond.value
            
            # Cases 1 and 2 (Granted):
            if not wrong_attr and not other_cond:
                resp[service+":"+action] = ""

            # Cases 3 and 4 (Granted with Conditions):
            elif not wrong_attr and other_cond and attr_match:
                if service+":"+action not in resp:      # This is the first policy
                    if condition.find("and") == -1:        # Includes the case: condition == ""
                        resp[service+":"+action] = condition
                    else:
                        resp[service+":"+action] = "(" + condition + ")"

                elif resp[service+":"+action] != "":   # The policy was not yet granted - combine with or
                    if condition.find("and") == -1:
                        resp[service+":"+action] = resp[service+":"+action] + " or " + condition
                    else:
                        resp[service+":"+action] = resp[service+":"+action] + " or (" + condition + ")"
#                else:  # If the policy was already granted, do nothing
#                    pass

            # Cases 5 and 6 (Not Granted) ==> wrong_attr
#            else: # If policy is not granted, do nothing.
#                pass
    return resp

# This function returns all actions that are allowed when the attributes from
# request matches and there is no other required.
def actions_2(queryset, attributes):

    attributes = json.loads(attributes)    #{"role": ["admin"], "attr2": [--list--]}

    resp = []
    for and_rule in queryset:
        if and_rule.enabled:

            other = False # Other unmatched condition(s) found

            service = ""
            action = ""

            for cond in and_rule.conditions.all():
                if cond.attribute == "service":
                    service = cond.value
                elif cond.attribute == "action":
                    action = cond.value
                elif cond.attribute in attributes:
                    if cond.value not in attributes[cond.attribute]:
                        other = True
                else:
                    other = True
            
            if not other:
                if service+":"+action not in resp:
                    resp = resp + [service+":"+action]

    return resp
