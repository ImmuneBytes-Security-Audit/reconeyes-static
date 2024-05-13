import sys
import main
sys.path.append('C:/Users/DELL/Documents/GitHub/mercury/')
from ImmuneLite_v1 import informational, runner
from termcolor import colored


def costly_loop(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []
  # pprint.pprint(nodes)
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = informational.variable_handler(main.su['children'][index])
  for i in range(0, len(nodes)):
    # pprint.pprint(nodes[i])
    try:  
      statement = nodes[i]['body']['statements']
      # pprint.pprint(statement)
      for j in range(0,len(statement)):
        if statement[j]['type'] == "ForStatement":
          for_statement = statement[j]['body']['statements']  
          # pprint.pprint(type(for_statement))  
          for k in range(0, len(for_statement)):
            if for_statement[k]['type'] == 'ExpressionStatement':
              expression = for_statement[k]['expression']
              # pprint.pprint(expression)
              if (expression['operator'] == "++" or expression['operator'] == "--" or expression['operator'] == "+="):
                if expression['main.subExpression']['name'] in primitive_variable_data.keys():
                  print(colored("\n[Informational] costly-loop. " + name_of_the_contract + '.' + nodes[i]['name'] + '() has costly operations inside a loop.' , "green"))
                  runner.info +=1
                  informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
                informational.detectors["costly-loop"] = informational.flags
              else:
                informational.detectors["costly-loop"] = None
        else:
          informational.detectors["costly-loop"] = None
    except:
      informational.detectors["costly-loop"] = None
   
def constable_states(name_of_the_contract):
    # print(control_flow)
    
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    informational.flags = []
    # print("\n[Optimizational] Variables that should be declared constant")
    try:
      control_flow, external_calls = informational.control_flow(name_of_the_contract)
      for i in range(0, len(nodes)):
        if nodes[i]['variables'][0]['typeName']['type'] == 'Mapping' or nodes[i]['variables'][0]['typeName']['type'] == 'ArrayTypeName' :
          continue
        if nodes[i]['type'] == 'StateVariableDeclaration' and nodes[i]['isConstant'] == False:
          var = nodes[i]['variables'][0]['name']
          values = control_flow.get(var)
          # print(var, values)

          if len(values) == 1:
            print(colored("\n[Optimization] constable-states. " , "green") + colored(str(name_of_the_contract) + '.' + str(var) + " should be constant" , "green"))
            runner.optimize += 1
            informational.flags.append(name_of_the_contract + '.' + str(var))
        informational.detectors["constable-states"] = informational.flags
    except:
      pass

def external_functions(name_of_the_contract):
   
  informational.flags = []
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = informational.variable_handler(main.su['children'][index])
  try: 
    visibilities = {}
    for key, value in function_data.items():
      if 'constructor' == key:
        continue
      visibilities[key] = value[5]
    internal_funcs = []

    # case 1: when function call is there in primitive variable initialization
    if len(primitive_variable_data) != 0:
      # print("here")   
      for key, value in primitive_variable_data.items():
        if '(FunctionCall)' in value[1]:
          # print("here")
          func_name = value[1].split(' (')[0]
          internal_funcs.append(func_name)
        else:
          # print("here")
          pass
    else:
      # print("here")
      pass
    
    # case 2: when function call is there in variable assignment inside a function

    # case 3: when function call is an argument of another function
    if len(function_member_data) != 0:  
      # print("here")
      func_name = ""
      for key, value in function_member_data.items():
        for k, v in value.items():
          if '(FunctionCall)' in v[0] :
            func_name = v[0].split(' (')[0]
          elif '(FunctionCall)' in v[1]:
            func_name = v[1].split(' (')[0]
          internal_funcs.append(func_name)
    else:
      pass

    for i in range(0, len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          try:
            # function call in return statement in ()
            if 'components' in statements[j].keys() and statements[j]['components'][0]['type'] == 'FunctionCall' :
              internal_funcs.append(statements[j]['components'][0]['expression']['name'])
            # function call in return statement 
            elif statements[j]['type'] == 'FunctionCall':
              internal_funcs.append(statements[j]['expression']['name'])
          except:
            pass
      except:
        pass
    
    # print("Internally called functions: " , internal_funcs)

    for key, value in visibilities.items():
      if value == 'public' and key not in internal_funcs:
        print(colored("\n[Optimization] external-functions. " + name_of_the_contract + '.' + key + "() can be declared external!" , "green"))
        runner.optimize += 1
        informational.flags.append(name_of_the_contract + '.' + key + "() ")
      informational.detectors["external-functions"] = informational.flags
  except Exception as e:
    informational.detectors["external-functions"] = None
    # print("Except is running with exception: " + str(e))

def incorrect_use_of_view(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(function_data)

  for i in range(0, len(nodes)):
    try:
      if nodes[i]['type'] != "FunctionDefinition":
        continue
      else:
        if nodes[i]['stateMutability'] == "view" or nodes[i]['stateMutability'] == None:
          statements = nodes[i]['body']['statements']
          returnParameters = function_data[nodes[i]['name']][4]['parameters']
          # pprint.pprint(returnParameters)
          if len(statements) == 1 and len(returnParameters) != 0: 
            print(colored("\n[Optimizational] incorrect-use-of-view. " + name_of_the_contract + '.' + nodes[i]['name'] + "() state mutability can be limited to pure.", "green" ))
            runner.optimize += 1
            informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + "()")
          informational.detectors["incorrect-use-of-view"] = informational.flags
    except:
      informational.detectors["incorrect-use-of-view"] = None

def immutable_state(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  # pprint.pprint(nodes)
  informational.flags = []

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = informational.variable_handler(main.su['children'][index])

  # pprint.pprint(constructor_member_data)

  for key, value in constructor_member_data.items():
    for k,v in value.items():
      if k in list(primitive_variable_data.keys()) and '(FunctionCall)' not in v[0]:
        print(colored("\n[Optimization] immutable-states. " + name_of_the_contract + '.' + k + " can be declared immutable." , "green"))
        runner.optimize += 1
        informational.flags.append(name_of_the_contract + '.' + k + " can be declared immutable.")
  
  if len(informational.flags) != 0:
    informational.detectors["immutable-states"] = informational.flags
  else:
    informational.detectors["immutable-states"] = None
