from pyeda.inter import *
import json
import re
import copy

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
        gbl[rk] = eval(rv)
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
