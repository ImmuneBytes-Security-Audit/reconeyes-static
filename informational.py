import pprint
import sys
from ImmuneLite_v1 import runner
from termcolor import colored
import main

global detectors 
detectors = {}

global flags
flags = []


def initialValue_handler(expression, type):  
    try:
        try:   
            # print("here")
            if expression['expression']['name'] == 'block' and expression['memberName'] == 'timestamp' or expression['memberName'] == 'hash':
                # print("here")
                initialValue = expression['expression']['name'] + '.' + expression['memberName']
                return initialValue
            elif expression['expression']['name'] == 'msg' and expression['memberName'] == 'sender':
                initialValue = expression['expression']['name'] + '.' + expression['memberName']
                return initialValue    
        except:         
            if 'int' in type:  
              # print("this is running")
              try: #for primitive datatypes
                if expression['name'] == 'now':
                  # print(expression['name'])
                  initialValue = expression['name']
                  return initialValue
                elif len(expression) == 3:
                    initialValue = expression['number']
                    return initialValue
                elif len(expression) == 4:
                    try:                   
                        if expression['isPrefix'] == True and expression['operator'] == '+':
                            initialValue = expression['operator'] + expression[
                                'main.subExpression']['number']
                            return initialValue
                            # print(initialValue)
                        else:
                            initialValue = expression['operator'] + expression[
                                'main.subExpression']['number'] 
                            return initialValue
                            # print(initialValue)
                    except:
                        if expression['right']['number'] == '0':
                            initialValue = expression['left'][
                                'number'] + expression[
                                    'operator'] + expression['right']['number']
                            
                            print(
                                colored("Warning : Divide by zero!", "yellow"))
                            return initialValue

              except: #for primitive datatypes in functions
                # print("here")
                if expression['type'] == 'NumberLiteral':
                  initialValue = expression['number']
                  return initialValue
                else:
                  if expression['type'] == 'FunctionCall':
                    # print(expression)
                    initialValue = str(expression['expression']['name']) + ' (FunctionCall)'
                    return initialValue
            elif ('string' in type) or ('bool' in type):
                # pprint.pprint(expression)
                if 'left' in expression:
                    if expression['operator'] == '==' and expression['right']['type'] == 'BooleanLiteral':
                      print(colored("\nComparison of a boolean variable to a boolean literal detected!","yellow"))
                      # errors.append("Detected: Comparison of a boolean variable to a boolean literal!")
                    # print("yay!")
                    initialValue = expression['left']['name'] + expression['operator'] + str(expression['right']['value'])
                    return initialValue
                elif expression['type'] == 'FunctionCall' and expression['expression']['type'] == 'MemberAccess':
                  initialValue = expression['expression']['memberName'] + '()'
                  return initialValue
                elif expression['type'] == 'UnaryOperation' and 'main.subExpression' in expression.keys():
                  # pprint.pprint(expression)
                  if expression['main.subExpression']['type'] == 'FunctionCall':
                    initialValue = expression['main.subExpression']['expression']['memberName'] + ' (FunctionCall)'
                    # print(initialValue)
                    return initialValue
                else:
                    # print("else is running")
                    initialValue = expression['value']
            # print("--------InitialValue : ", end="")
            # pprint.pprint(initialValue)
                    return initialValue
            elif 'bytes' in type:
              try:
                # print("here")
                initialValue = expression['number']
                return initialValue
              except:
                try:
                  if expression['name'] == 'now':
                    # print(expression['name'])
                    initialValue = expression['name']
                    return initialValue 
                except:
                  if expression['type'] == 'FunctionCall':
                    # print(expression['expression']['memberName'])
                    initialValue = expression['expression']['memberName'] + ' (FunctionCall)'
                    # print(initialValue)
                    return initialValue
            elif 'address' in type:
              # print("here")
              try:
                # print(expression)
                if 'number' in expression.keys():
                  initialValue = expression['number']
                elif expression['type'] == 'MemberAccess':
                   initialValue = expression['name'] + '.' + expression['memberName']
                # print(initialValue)
                return initialValue
              except:
                pass
    except Exception as e:
        # print("CORRECT ONE")
        if expression['type'] == 'FunctionCall':  #then dont show the error as it may be a function call assigned.
            initialValue = expression['expression']['name'] + ' (FunctionCall)'
            return initialValue
        else:
            print(
                colored(
                    "\nAn error occured in informational.py in function initialValue_handler while extracting initial values (Line 8-48) : ",
                    'green'), colored(e, "red"))

#here the function will be defined.
def variable_handler(contract):
    try:
        nodes = contract['subNodes']
        primitive_variable_data = {}
        userDefined_member_data = {}
        function_member_data = {}
        constructor_member_data = {}
        function_data = {}
        constructor_data = {}
        member_data = {}
        requires = []
        constant_variables = []        

        if len(nodes) == 0:
            return 'The contract is empty'

        for index in range(0, len(nodes)):
            
            if 'libraryName' in nodes[index].keys():
              continue
            # pprint.pprint(nodes[index]['name'])
            
            try:  
                #try is for primitive datatypes
                # print("heereeeeeeee")
                variable_name = nodes[index]['variables'][0]['name']  #it is printing down
                # print(variable_name)
                isDeclaredConst = nodes[index]['variables'][0]['isDeclaredConst']
                isStateVar = nodes[index]['variables'][0]['isStateVar']
                visibility = nodes[index]['variables'][0]['visibility']
                if 'stateMutability' in nodes[index]['variables'][0]['typeName'].keys():
                  stateMutability = nodes[index]['variables'][0]['typeName']['stateMutability']
                else:
                  stateMutability = None
                try:
                    # print("in")
                    # for non-primitive datatypes like Victim v;
                    if 'namePath' in nodes[index]['variables'][0]['typeName'].keys():
                      variable_datatype = nodes[index]['variables'][0]['typeName']['namePath']
                    else:
                      variable_datatype = nodes[index]['variables'][0]['typeName']['name']
                    data = []
                    data.append(variable_datatype)
                    # print(data)
                    expression = nodes[index]['variables'][0]['expression']

                    if nodes[index]['initialValue'] != None:
                        variable_initialValue = initialValue_handler(
                            expression, variable_datatype)
                        # print(variable_initialValue)  
                        data.append(variable_initialValue)
                        if len(nodes[index]['variables'][0]['typeName']) == 3: #for handling address's stateMutability
                          data.append(nodes[index]['variables'][0]['typeName']['stateMutability'])
                        data.append(isDeclaredConst)
                        data.append(isStateVar)
                        data.append(visibility)

                        primitive_variable_data[variable_name] = data
                        if data[2] == True:
                            constant_variables.append(variable_name)
                    else:
                        data = [
                            variable_datatype, "uninitialized",
                            isDeclaredConst, isStateVar, visibility, stateMutability
                        ]
                        primitive_variable_data[variable_name] = data
                        # print(primitive_variable_data)
                except:  #if this is executed, that means it is an array
                  try:
                    if 'namePath' in nodes[index]['variables'][0][
                        'typeName']['baseTypeName'].keys():
                      variable_datatype = nodes[index]['variables'][0][
                        'typeName']['baseTypeName']['namePath']
                    else:
                      variable_datatype = nodes[index]['variables'][0][
                        'typeName']['baseTypeName']['name']
                    # print(variable_datatype)
                    data = ['array']
                    data.append(variable_datatype)
                    members = []
                    isDeclaredConst = nodes[index]['variables'][0]['isDeclaredConst']
                    if nodes[index]['initialValue'] != None:
                        components = nodes[index]['variables'][0][
                            'expression']['components']
                        for component in components:
                            members.append(
                                initialValue_handler(component, variable_datatype))
                        data.append(members)
                        data.append(isDeclaredConst)
                        data.append(isStateVar)
                        data.append(visibility)
                        primitive_variable_data[variable_name] = data
                    else:
                        d = [
                            'array', variable_datatype, "uninitialized",
                            isDeclaredConst, isStateVar, visibility
                        ]
                        primitive_variable_data[variable_name] = d
                    try:

                        array_length = nodes[index]['variables'][0][
                            'typeName']['length']['number']
                        array_length = int(array_length)
                        if len(members) != array_length:
                            print("\nArray '", variable_name,
                                  "' has some unused memory!\n")
                            # errors.append("Detected! Array has some unused memory. Array: " + str(variable_name))
                    except:  # handle an uninitialized array
                        pass
                  except: 
                    try: #for mappings
                      # print("here")
                      data = []
                      variable_datatype = nodes[index]['variables'][0]['typeName']['type']
                      data.append(variable_datatype)
                      isDeclaredConst = nodes[index]['variables'][0]['isDeclaredConst']
                      keyType = nodes[index]['variables'][0]['typeName']['keyType']['name']
                      # print(keyType)
                      if 'namePath' in nodes[index]['variables'][0]['typeName']['valueType']:
                        valueType = nodes[index]['variables'][0]['typeName']['valueType']['namePath']
                        # print(valueType)
                        data.append([keyType, "struct: " + str(valueType)])
                      elif 'valueType' in nodes[index]['variables'][0]['typeName']['valueType']:
                        # print("nested mapping")
                        valueType = nodes[index]['variables'][0]['typeName']['valueType']['type']
                        # print(valueType)
                        data.append([keyType, "nested mapping: " + str(valueType)])
                      else:
                        valueType = nodes[index]['variables'][0]['typeName']['valueType']['name']
                      # print(valueType)
                        data.append([keyType, valueType])
                      data.append('uninitialized')
                      data.append(isDeclaredConst)
                      data.append(isStateVar)
                      data.append(visibility)
                      # print(data)
                      variable_name = nodes[index]['variables'][0]['name']
                      primitive_variable_data[variable_name] = data
                      # print(primitive_variable_data)
                      
                    except: #for two-dimensional arrays
                      # print("this is running")
                      data = []
                      variable_datatype = nodes[index]['variables'][0]['typeName']['baseTypeName']['baseTypeName']['name']
                      # print(variable_datatype)
                      data = ['two-dimensional array']
                      data.append(variable_datatype)
                      members = []
                      isDeclaredConst = nodes[index]['variables'][0]['isDeclaredConst']
                      if nodes[index]['initialValue'] != None:
                        # print("here")
                        components = nodes[index]['variables'][0]['expression']['components']
                        # print(len(components))
                        big = []
                        for x in range(0, len(components)):
                          # print(x)
                          arr = []
                          for c in range(0, len(components[x]['components'])):
                            # print(components[x]['components'][c]['number'])
                            arr.append(components[x]['components'][c]['number'])
                          big.append(arr)
                          # print("big: ", big)
                        data.append(big)
                        # print(data)
                        data.append(isDeclaredConst)
                        data.append(isStateVar)
                        data.append(visibility)
                        primitive_variable_data[variable_name] = data
                        # print(primitive_variable_data)
                      
            except:  #except is for user-defined datatypes
                #for user-defined data types we have to access elements with it
                #both are defined differently because they have different structures

                name = nodes[index]['name']
                # print(name)
                try:  # it is for extracting variable names
                    # pprint.pprint(nodes[index]['members'])
                    # print("here")
                    if nodes[index]['type'] == 'StructDefinition':
                      member_data = {}
                      for member in range(0, len(nodes[index]['members'])):
                          # print(member)                       
                          member_type = []
                          member_name = (nodes[index]['members'][member]['name'])
                          if len(nodes[index]['members'][member]['typeName']) == 3:
                            member_type.append(nodes[index]['members'][member]['typeName']['type'])
                          elif 'namePath' in nodes[index]['members'][member]['typeName']: #nested structure
                            member_type.append("struct: "+str(nodes[index]['members'][member]['typeName']['namePath']))
                          else:
                            member_type.append(nodes[index]['members'][member]['typeName']['name'])
                          # print(member_type)
                          member_type.append(nodes[index]['members'][member]['storageLocation'])
                          member_data[member_name] = member_type
                          userDefined_member_data[name] = member_data
                          # pprint.pprint(userDefined_member_data)
                    elif nodes[index]['type'] == 'EnumDefinition':
                      member_names = []
                      member = nodes[index]['members']
                      for i in range(0, len(member)):
                        member_names.append(member[i]['name'])
                      # print(member_names)
                      userDefined_member_data[name] = member_names                
                    else: #so that except gets executed
                      x = 2/0
                except:  #for functions 
                  # print("here")
                  try:
                    if len(nodes[index]['body']) == 0:
                      continue
                  except:
                    pass
                  
                  try:
                    visibility = nodes[index]['visibility']  
                    isFallback = nodes[index]['isFallback']
                    isReceive = nodes[index]['isReceive']
                    modifiers = nodes[index]['modifiers']
                    parameters = nodes[index]['parameters']
                    returnParameters = nodes[index]['returnParameters']
                    stateMutability = nodes[index]['stateMutability']

                  except: # in case of modifiers, these wont be there
                    visibility = None  
                    isFallback = None
                    isReceive = None
                    modifiers = None
                    parameters = None
                    returnParameters = None
                    stateMutability = None

                  # print("here")
                  if nodes[index]['type'] == 'EventDefinition':
                    # print(contract['name'])
                    event_handler(name)

                  elif nodes[index]['type'] == 'FunctionDefinition' and nodes[index]['name'] != contract['name'] :
                  # and nodes[index]['isConstructor'] == False:
                    # print("here")


                    statements = nodes[index]['body']['statements'] 
                    if len(statements) == 0:
                          function_type = "Empty function"
                    else:
                      function_type = "Implemented function"   
                    
                    try:
                      if len(statements) == 0:
                        event_name = "Event: "
                      else:
                        for j in range(0, len(statements)):
                          if statements[j]['type'] == 'EmitStatement':
                            event_name = "Event: " + statements[j]['eventCall']['expression']['name']     
                          else:
                            # print("here")
                            event_name = "Event: "
                        # print(event_name)
                    except:
                      # print("here")
                      event_name = "Event: "

                    function_data[name] = [
                            isFallback, isReceive, modifiers, parameters, returnParameters, 
                            visibility, stateMutability, function_type, event_name
                        ]
                    function_members = {}
                    # function_member_data_list = []
                    count = 0
                    
                    for statement in statements:
                        # pprint.pprint(statement)             
                        try: 
                          if 'variables' in statement.keys():
                              function_member_data_list = []
                              member_type = statement['variables'][0]['typeName']['name']
                              # print(member_type)
                              member_data = statement['initialValue']
                              function_member_data_list.append(member_type)
                              # pprint.pprint(member_data)
                              if member_data != None:  
                                # print("//////", initialValue_handler(member_data, member_type))
                                function_member_data_list.append(initialValue_handler(member_data, member_type))
                                function_members[statement['variables'][0]['name']] = function_member_data_list
                                function_member_data_list.append(statement['variables'][0]['storageLocation'])
                                # print("---------",function_member_data_list)
                              else:
                                function_member_data_list.append("uninitialized")
                                function_member_data_list.append(statement['variables'][0]['storageLocation'])
                              
                              function_members[statement['variables'][0]['name']] = function_member_data_list
                              # print("This is function_members : ",function_members)
                              if nodes[index][
                                      'isConstructor'] == True:  #this means this is a constructor
                                  count += 1
                                  if len(constructor_member_data) > 0:
                                      constructor_member_data[
                                          name] = function_members
                                  else:
                                      constructor_member_data[
                                          name+str(count)] = function_members
                              else:
                                  function_member_data[name] = function_members

                          elif statements[j]['type'] == 'ExpressionStatement' and statement['expression']['operator'] == '=':
                            # print("here")
                            function_member_data_list = []
                            # constructor_member_data = {}
                            function_member_data_list.append(statement['expression']['right']['expression']['name'] + '.' + statement['expression']['right']['memberName'])
                            function_members[statement['expression']['left']['name']] = function_member_data_list

                            if nodes[index]['isConstructor'] == True:
                              # print("here")
                              constructor_member_data[nodes[index]['name']] == function_member_data_list

                            else:
                              function_member_data[name] = function_members   
                            # print(function_member_data_list)

                          # #for redundant statements
                          # elif 'expression' in statement.keys() and (statement['expression']['type'] == 'ElementaryTypeName' or statement['expression']['type'] == 'Identifier'):
                          #   redundancy.append((statement['expression']['name']))
                          #   print(redundancy)

                          # if statement['type'] == 'IfStatement' and ( statement['condition']['type'] == 'BooleanLiteral' or (
                          #   statement['condition']['operator'] == '||' and 
                          #   statement['condition']['right']['type'] == 'BooleanLiteral') or (
                          #   statement['condition']['operator'] == '!' and
                          #      statement['condition']['main.subExpression']['type']
                          #      == 'BooleanLiteral')):
                          #     print(colored("Warning!! Missuse of boolean constant detected in function!", "yellow"))

                          elif 'expression' in statement.keys() and statement['expression']['right']['isArray'] == True:
                            arr_value = []
                            function_member_data_list = []
                            # function_member_data = {}
                            var_name = statement['expression']['left']['name']
                            function_member_data_list.append("array")
                            for a in range(0, len(statement['expression']['right']['components'])):
                              if 'operator' in statement['expression']['right']['components'][a] and 'operator' in statement['expression']['right']['components'][a]['operator'] == '-':
                                if 'signed' in function_member_data_list:
                                  pass
                                else:
                                  function_member_data_list.append("signed")
                                arr_value.append(statement['expression']['right']['components'][a]['operator'] + statement['expression']['right']['components'][a]['main.subExpression']['number'])
                              elif statement['expression']['right']['components'][a]['main.subdenomination'] == None:
                                arr_value.append(statement['expression']['right']['components'][a]['number'])
                            # print(arr_value) 
                            function_member_data_list.append(arr_value)
                            function_members[var_name] = function_member_data_list
                            function_member_data[name] = function_members
                            # print(function_members)                           
                          else:
                            x = 2/0
                        except: #for function calls inside functions
                          try:
                            # print("try run")
                            function_member_data_list = []
                            # function_member_data = {}
                            if 'expression' in statement and statement['expression']['type'] == 'FunctionCall':
                              # print("yes")  
                              func_name = statement['expression']['expression']['memberName']
                              arguments = []
                              for argument in statement['expression']['arguments']:
                                try:
                                  if argument['type'] == 'FunctionCall':
                                    arguments.append(str(argument['expression']['name']) + '(' + str(argument['arguments'][0]['name']) + ')')
                                  elif argument['type'] == 'MemberAccess':
                                    arguments.append(str(argument['expression']['name']) + '.' + str(argument['memberName']))
                                  else:
                                    arguments.append(argument['name'])
                                except:
                                  pass
                              # print(arguments)
                              function_member_data_list.append(argument ['expression']['name'] + " (FunctionCall)")
                              function_member_data_list.append(arguments)
                              function_members[func_name] = function_member_data_list
                              function_member_data[name] = function_members

                            elif 'expression' in statement.keys() and statement['expression']['right']['type'] == 'FunctionCall':
                              # print("here")
                              var_name = statement['expression']['left']['name']
                              func_name = statement['expression']['right']['expression']['name']

                              function_member_data_list.append(func_name + " (FunctionCall)")
                              function_members[var_name] = function_member_data_list
                              if nodes[index]['isConstructor'] == True:
                                constructor_member_data['constructor'] = function_members
                                    # print("here")
                              else:
                                function_member_data[name] = function_members
                                # print(function_member_data)                
                            else:
                              # print("here")
                              x = 2/0
                          except:
                            # print("this is running")
                            try:
                              # pprint.pprint(nodes[index]['name'])
                              if statement['expression']['type'] == 'FunctionCall':
                                if statement['expression']['expression']['name'] == 'require':
                                  # print("here")
                                  # print(contract['name'])
                                  requires = runner.require_handler(contract['name'])
                                  # print(f)
                              else:
                                # print("ok")
                                x = 2/0
                            except:
                              # print("except")
                              try:
                                # print("here")
                                function_member_data_list = []

                                if 'expression' in statement.keys() and statement['expression']['operator'] == '=' and statement['expression']['left']['type'] == 'Identifier' and statement['expression']['right']['type'] == 'Identifier' :
                                  function_member_data_list.append(statement['expression']['right']['type'])
                                  function_member_data_list.append(statement['expression']['right']['name'])
                                  function_members[statement['expression']['left']['name']] = function_member_data_list

                                  if nodes[index]['isConstructor'] == True:
                                    constructor_member_data['constructor'] = function_members
                                    # print("here")
                                  else:
                                    function_member_data[name] = function_members

                                elif 'expression' in statement.keys() and statement['expression']['operator'] == '=' and statement['expression']['left']['type'] == 'Identifier' and statement['expression']['right']['type'] == 'MemberAccess' :

                                  function_member_data_list.append(statement['expression']['right']['type'])

                                  function_member_data_list.append(statement['expression']['right']['expression']['name'] + '.' + statement['expression']['right']['memberName'])
                                  function_members[statement['expression']['left']['name']] = function_member_data_list

                                  if nodes[index]['isConstructor'] == True:
                                    constructor_member_data['constructor'] = function_members
                                    # print("here")
                                  else:
                                    function_member_data[name] = function_members
                              except:
                                # print("here")
                                try:
                                  print(statement['expression']['left'])
                                  if statement['expression']['left']['type'] == 'Identifier' and statement['expression']['right']['type'] == 'Identifier' :
                                    print("this")
                                except:
                                  pass


                  elif nodes[index]['type'] == 'ModifierDefinition':
                    # print("here")
                    modifiers = modifier_handler(contract['name'])
                    # print(modifier)

                  # for constrcutors 
                  # in 4.22 --- constructors could be defined both as function <contract name>() and through contructor keyword
                  elif nodes[index]['name'] == contract['name'] or nodes[index]['isConstructor'] == True:
                    constructor_data[name] = [ isFallback, isReceive, modifiers, parameters, returnParameters, visibility, stateMutability ] 

                    # constructor_member_data = 
                  else:
                    # print("last else")
                    pass
                        
            # print(name," : ",initialValue,"\n")
            # pprint.pprint(name)
        # print("\n\nPrinting User defined variable data :")
        # pprint.pprint(userDefined_member_data)
        # print(colored("\n\nPrimitive type Variables in the contract :",
        #               'cyan'))
        # pprint.pprint((primitive_variable_data))
        # print(colored("\n\nFunction members: ", 'cyan'), function_member_data)
        # print(colored("\n\nConstructor members: ", 'cyan'),
        #       constructor_member_data)
        # print(colored("\nFunction Data: ", 'cyan'))
        # pprint.pprint(function_data)
        # print("Requires in the contract:")
        # pprint.pprint(requires)
       
        # if len(constructor_member_data) > 1:
        #     # print(colored("\nWARNING!! More than one constructors detected.","yellow"))
        #     errors.append("Detected! More than one constructor is present!")
        
        # print("\nThese are the constant variables: ", constant_variables)

        return userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires
    except Exception as e:
        print(
            colored(
                "\nAn error occured in informational.py in function variable_handler while handling variables (Line 43-234) : ",
                "green"), colored(e, "red"))


def event_handler(name_of_the_contract):
  try:
     
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    # print(name_of_contracts)
    # print("Index",index)
    # print(main.su['children'][index]['name'])
    event_list = []
    for i in range(0, len(nodes)):
      try:
        if nodes[i]['type'] == 'EventDefinition':
          event_list.append(nodes[i]['name'])
      except:
        continue
    # print("Events: ", event_list)
    return event_list
  except:
    pass

def modifier_handler(name_of_the_contract):
  try:
     
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    modifier_list = []
    for i in range(0, len(nodes)):
      try:
        if nodes[i]['type'] == 'ModifierDefinition':
          modifier_list.append(nodes[i]['name'])
          statements = nodes[i]['body']['statements']
          for j in range(0, len(statements)):
            try:
              if statements[j]['expression']['type'] == 'FunctionCall' and statements[j]['expression']['expression']['name'] == 'require':
                modifier_list = runner.require_handler(name_of_the_contract)
              else:
                pass
            except:
              modifier_list = runner.require_handler(name_of_the_contract)
      except:
        continue
    # print("Modifiers: ", modifier_list)
    return modifier_list
  except:
    pass

def redundant_statements(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  redundancy = []
  for i in range(0, len(nodes)):
    try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          if 'expression' in statements[j].keys() and ((statements[j]['expression']['type'] == 'ElementaryTypeName' or statements[j]['expression']['type'] == 'Identifier')):
            if statements[j]['expression']['name'] == '_':
              continue
            redundancy.append((statements[j]['expression']['name']))
            # print(redundancy)
    except:
      pass
  if len(redundancy) !=0:
    for i in redundancy:
      print(colored("\n[Informational] redundant-statements. Redundant expression: " + i + " in " + name_of_the_contract, "green"))
      flags = [i + " in " + name_of_the_contract]
    detectors["redundant_statements"] = flags
  else:
    detectors["redundant_statements"] = None

def dead_code(name_of_the_contract):
     
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    # print(name_of_contracts)
    flags = []
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = variable_handler(main.su['children'][index])
    funcs = list(function_data.keys())
    children_str = str(main.su['children'])
    # print(children_str)
    for f in funcs:
      if f == 'constructor':
        detectors["dead-code"] = None
        continue

      if children_str.count(f) == 1 and (function_data[f][5] != 'external' and function_data[f][5] != 'public'):
        # print(f)
        print(colored("\n[Informational] dead-code. " + name_of_the_contract + '.' + f + "() is never used and should be removed." , "green"))
        runner.low += 1
        flags = [name_of_the_contract + '.' + f + "() is never used and should be removed."]
        detectors["dead-code"] = flags
      else:
        detectors["dead-code"] = None


def too_many_digits(name_of_the_contract):
    
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    flags = []
    userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data , constructor_data, requires = variable_handler(main.su['children'][index])

    #extract variable name and value
    try:
      for key, value in primitive_variable_data.items():
          if value[1] == None:
            continue
          if 'address' in value[0]:
            continue

          if 'int' in value[0]:
              initialValue = value[1]
              occurance = initialValue.count('0')
              if occurance <= 4:
                  continue
              if int(initialValue[0]) >= 1 and int(initialValue[0]) <= 9 :
                  print(colored( "\n[Informational] too-many-digits. " , "green") + colored(name_of_the_contract + "." + key + " uses literals with too many digits", "green"))
                  runner.info +=1
                  flags = [name_of_the_contract + "." + key + " uses literals with too many digits"]
                  detectors["too-many-digits"] = flags
          else:
            detectors["too-many-digits"] = None
    except:
      detectors["too-many-digits"] = None



    for i in range(0, len(nodes)):
      # print("here")
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          stmt_str = str(statements[j])
          # print(stmt_str)
          lst = stmt_str.split(' ')
          # pprint.pprint(lst)
          for k in lst:
            if '0x' in k:
              continue
            if '00000' in k:
              print(colored( "\n[Informational] too-many-digits. " , "green") + colored(name_of_the_contract + "." + nodes[i]['name'] + "() uses literals with too many digits", "green"))
              flags = [name_of_the_contract + "." + key + " uses literals with too many digits"]
              detectors["too-many-digits"] = flags
              runner.info +=1
      except:
        flags = [name_of_the_contract + "." + key + " uses literals with too many digits"]
        detectors["too-many-digits"] = flags

def block_timestamp(name_of_the_contract):
     
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    flags = []
    userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data , constructor_data, requires = variable_handler(main.su['children'][index])
    # pprint.pprint(primitive_variable_data)

    for key, value in primitive_variable_data.items():
        if value[1] == 'timestamp':
            print(colored("\n[Low] block.timestamp. ", "green") + colored( name_of_the_contract + '.' + key + " uses block.timestamp." , "green" ))
            flags = [name_of_the_contract + '.' + key + "uses block.timestamp."]
            detectors["block-timestamp"] = flags
            runner.low += 1

    for i in range(0, len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          stmt_str = str(statements[j])

          if 'timestamp' in stmt_str:
            print(colored("\n[Low] block.timestamp. ", "green") + colored( name_of_the_contract + '.' + nodes[i]['name'] + "() uses block.timestamp." , "green" ))
            flags = [name_of_the_contract + '.' + nodes[i]['name'] + "() uses block.timestamp."]
            detectors["block-timestamp"] = flags
            runner.low += 1
      except:
        detectors["block-timestamp"] = None


def unused_state_variable(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  flags = []
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data , constructor_data, requires = variable_handler(main.su['children'][index])
  # pprint.pprint(primitive_variable_data)
  lst = list(primitive_variable_data.keys())
  count = 0
  for l in lst:
      # print(l)
      try:
        nodes = str(main.su['children'][index])
        if l in nodes:
          count = nodes.count(l)
      except:
        pass
      if count == 1:
        print(colored("\n[Informational] unused-state-variable. " + name_of_the_contract + '.' + l + " is never used in " + name_of_the_contract , "green"))
        runner.info += 1
        flags = name_of_the_contract + '.' + l + " is never used"
        detectors["unused-state-variable"] = flags

def control_flow_graph(name_of_the_contract):
     
    control_flow = {}
    variable_sequence = []
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    #check if the contract is empty
    if len(nodes) == 0:
        return
    for i in range(0, len(nodes)):
      # print(len(nodes))
      try:
        if nodes[i]['type'] == 'StateVariableDeclaration':
            variable_datatype = nodes[i]['variables'][0]['typeName']['name']
            expression = nodes[i]['variables'][0]['expression']
            # print(variable_datatype, "------",expression)

            # in case of state variable initialization and when the variable is already present in the control flow list
            if nodes[i]['initialValue'] != None:
              variable_sequence.append(nodes[i]['variables'][0]['name'])
              if control_flow.get(nodes[i]['variables'][0]['name']):
                # print("Printing", control_flow.get(nodes[i]['variables'][0]['name']))
                new_value = control_flow.get(nodes[i]['variables'][0]['name'])
                new_value.append(initialValue_handler(expression, variable_datatype))
                # print(new_value)
                control_flow[nodes[i]['variables'][0]['name']] = new_value
              else:
                # print("here")
                control_flow[nodes[i]['variables'][0]['name']] = [ initialValue_handler(expression, variable_datatype)]
                # print(control_flow)
            else:
              variable_sequence.append([nodes[i]['variables'][0]['name']])
              control_flow[nodes[i]['variables'][0]['name']] = []

        elif nodes[i]['type'] == 'FunctionDefinition':
            function_member = []
            member_dict = {}
            # pprint.pprint(nodes[i])
            # print("HERE")
            statements = nodes[i]['body']['statements']
            function_member_data = []
            for statement in statements:
                # function_member_data = []
                try:
                  exp = statement['expression']
                  if exp['operator'] == '=':
                    function_member.append((exp['left']['name']))
                    function_member_data.append(exp['right']['number'])
                    member_dict[exp['left']['name']] = function_member_data
                  # pprint.pprint(function_member)
                  control_flow[function_name] = member_dict
                except:
                  # print("run")
                  # pass
                  member_type = statement['variables'][0]['typeName']['name']
                  member_data = statement['initialValue']
                  function_name = nodes[i]['name']
                  member_name = statement['variables'][0]['name']
                  function_member.append(member_name)
                  if statement['initialValue'] != None:
                      # print("running")
                      if member_dict.get(member_name):
                          new_value = member_dict.get(member_name)
                          # print(initialValue_handler(member_data, member_type))
                          new_value.append(
                              initialValue_handler(member_data, member_type))
                          member_dict[member_name] = new_value
                          # print(member_dict)
                      else:
                          # print("else")
                          function_member_data = []
                          function_member_data.append(
                              initialValue_handler(member_data, member_type))
                          member_dict[member_name] = function_member_data
                          # print(member_dict)
                  else:
                      member_dict[member_name] = []

                  control_flow[function_name] = member_dict
            
        variable_sequence.append(tuple(function_member))

      except:
        pass

    # print("\nControl Flow: ", control_flow)
    # print("\nVariable Sequence: ",variable_sequence)
    return control_flow, variable_sequence

def function_init_state(name_of_the_contract):
   
  flags = []
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires  = variable_handler(
        main.su['children'][index])
  # pprint.pprint(primitive_variable_data)
  try:
    for key, value in primitive_variable_data.items():
      try:
        if "(FunctionCall)" in value[1]:
          print(colored("\n[Informational] Function initializing state variable: " + key , "green"))
          runner.info +=1
          flags.append(key)
      except:
        continue

    for key,value in function_member_data.items():
          # print(value)
          for k,v in value.items():
            if "(FunctionCall)" in v[1]:
              print(colored("\n[Informational] Function initializing state variable: " + key , "green"))
              runner.info +=1
              flags.append(key)
    detectors["function-init-state"] = flags
  except:
    pass
  
def unimplemented_function(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  # print("Index: ", index)
  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constructor_data, requires = variable_handler(main.su['children'][index])
  baseContracts = []
  unimplemeted_function_list = []
  interfaces_dict = runner.interfaces()
  # print(interfaces_dict)f
  flags = []
  try:  
    if len(main.su['children'][index]['baseContracts']) != 0:
      for i in range(0, len(main.su['children'][index]['baseContracts'])):
        name = main.su['children'][index]['baseContracts'][i]['baseName']['namePath']
        baseContracts.append(name)
        keys = list(function_data.keys())
        for key,value in function_data.items():
          # print("Key: ", key, "\nValue: ", value)
          if (key in interfaces_dict[baseContracts[i]] and value[6] == "Empty function"):
            unimplemeted_function_list.append(key)
          else:
            continue
        for c in interfaces_dict[baseContracts[i]]:
          if c not in keys:
             unimplemeted_function_list.append(c)
      for i in unimplemeted_function_list:
        print(colored("\n[Informational] unimplemented-functions. " + name_of_the_contract + " does not implement function " + i + "()", "green"))
        flags.append(i)
      detectors["unimplemented-functions"] = flags
  except:
    detectors["unimplemented-functions"] = None


def assembly(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  # print("Index: ", index)
  nodes = main.su['children'][index]['subNodes']
  flags = []
  for i in range(0, len(nodes)):
    # print(nodes[i]['name'])
    count = 0
    try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          stmt = str(statements[j])
          if 'AssemblyBlock' in stmt:
            print(colored("\n[Informational] assembly. " + name_of_the_contract + '.' + nodes[i]['name'] + '() uses assembly.' , "green"))
            runner.info += 1
            flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
        detectors['assembly'] = flags
    except:
      detectors['assembly'] = None


def low_level_calls(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  flags = []
  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constructor_data, requires  = variable_handler(main.su['children'][index])
  # pprint.pprint(function_member_data)
  
  lowLevelCalls = ['delegatecall', 'call', 'callcode']
  for i in range(0, len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for statement in statements:
        try:
          if statement['expression']['type'] != 'FunctionCall':
            # print(statement['type'])
            if statement['type'] == 'ForStatement':
              # print("here")
              exp_str = str(statement['expression'])
              # pprint.pprint(exp_str)
              for l in low_level_calls:
                if l in exp_str:
                  print(colored("\n[Informational] low-level-calls. " + name_of_the_contract + '.' + nodes[i]['name'] + '() contains a low level call.' , "green"))
                  runner.info += 1
                  flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
          else:
            try:
              # print("here")
              if statement['expression']['expression']['memberName'] in lowLevelCalls:
                print(colored("\n[Informational] low-level-calls. " + name_of_the_contract + '.' + nodes[i]['name'] + '() contains a low level call.' , "green"))
                runner.info += 1
                flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
            except:
              pass        
        except:
          try:
            for key,value in function_member_data.items():
              # print("in")
              for k,v in value.items():
                if v[1].split(' ')[0] in lowLevelCalls:
                  print(colored("\n[Informational] low-level-calls. " + name_of_the_contract + '.' + key + '() contains a low level call.', "green"))
                  runner.info += 1
                  flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
          except:
            if statement['type'] == 'ForStatement':
                exp_str = str(statement['body']['statements']['expression'])
                for l in low_level_calls:
                  if l in exp_str:
                    print(colored("\n[Informational] low-level-calls. " + name_of_the_contract + '.' + nodes[i]['name'] + '() contains a low level call.' , "green"))
                    runner.info += 1
                    flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
      detectors['low-level-calls'] = flags
    except:
      detectors['low-level-calls'] = None

def erc20_indexed(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  flags = []
  event_list = ['Transfer', 'Approval']

  for i in range(0, len(nodes)):
    try:
      if 'ERC20.sol' in runner.imports:
        if nodes[i]['type'] == 'EventDefinition' and nodes[i]['name'] in event_list:     
          parameters = nodes[i]['parameters']['parameters']
          if parameters[0]['isIndexed'] == False or parameters[1]['isIndexed'] == False:
            print(colored("\n[Informational] erc20-indexed. " + name_of_the_contract + '.' + nodes[i]['name'] + " should have the indexed keyword." , "green"))
            runner.info += 1
            flags.append([name_of_the_contract + '.' + nodes[i]['name']])
      detectors["erc20_indexed"] = flags
    except:
      detectors["erc20_indexed"] = None
      

def depracacted_standards(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  flags = []
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = variable_handler(main.su['children'][index])
  # pprint.pprint(requires)

  #1 Deprecated standard: block.blockhash()
  # case 1: bytes32 b = block.blockhash(0);
  try:
    for key, value in primitive_variable_data.items():
      if 'blockhash' in value[1]:
        print("\nblock.blockhash() used in variable: '" + key + "' is deprecated!")
        flags.append("block.blockhash() used in variable: '" + key )
  except:
    pass

  # case 2: if bytes32 b = block.blockhash(0) is in a function
  try:
    for key, value in function_member_data.items():
      for k,v in value.items():
        if 'blockhash' in v[1]:
          print("\nblock.blockhash() used in variable: '" + k + "' in function: " + key + "()' is deprecated!")
          flags.append("block.blockhash() used in variable: '" + k + "' in function: " + key + "()" )
  except:
    pass

  #2 Deprecated standard: use of constant as stateMutability
  try:
    for key, value in function_data.items():
      if 'constant' in value:
        print("\nUse of constant is deprecated! Change the state mutability to pure/view in function: " + key + '()')
        flags.append("Use of constant is deprecated! Change the state mutability to pure/view in function: " + key + '()' )
  except:
    pass

  #3 Deprecated standard: use of sha3
  try:
    for key, value in function_member_data.items():
      for k,v in value.items():
        if 'sha3' in v[1]:
          print("\nUse of sha3 has been deprecated. Use keccak256() in function: '" + key + "()' in variable: '" + k + "'")
          flags.append("Use of sha3 has been deprecated. Use keccak256() in function: '" + key + "()' in variable: '" + k + "'")
  except:
    pass

  #4 Deprecated standard: main.suicide()
  try:
    for i in range(0, len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          try:
            if 'expression' in statements[j].keys() and statements[j]['expression']['type'] == 'FunctionCall':
              if statements[j]['expression']['expression']['name'] == 'main.suicide':
                print("\nUse of main.suicide() has been deprecated! Use 'selfdestruct()' in function: '" + nodes[i]['name'] + "()'")
                flags.append("Use of main.suicide() has been deprecated! Use 'selfdestruct()' in function: '" + nodes[i]['name'] + "()")
          except:
            continue
      except:
        pass
  except:
    pass
  
  #4 Deprecated standard: callcode()
  try:
    for i in range(0, len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          try:
            if 'expression' in statements[j].keys() and statements[j]['expression']['expression']['memberName'] == 'callcode':
              print("\nUse of callcode() has been deprecated! Use 'delegatecall()' in function: '" + nodes[i]['name'] + "()'")
              flags.append("Use of callcode() has been deprecated! Use 'delegatecall()' in function: '" + nodes[i]['name'] + "()")
          except:
            continue
      except:
        pass
  except:
    pass

  #5 Deprecated standard: throw
  try:
    for i in range(0, len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          try:
            if statements[j]['type'] != 'IfStatement':
              continue
            else:
              if_statements = statements[j]['TrueBody']['statements']
              for k in range(0, len(if_statements)):
                if if_statements[k]['type'] == 'ThrowStatement':
                  print("Use of throw has been deprecated! Use revert in function: " + nodes[i]['name'] + '()')
                  flags.append("Use of throw has been deprecated! Use revert in function: " + nodes[i]['name'] + '()')
          except:
            continue
      except:
        pass
  except:
    pass

  #6 Deprecated standard: msg.gas 
  # case 1 msg.gas is in require
  try:
    for i in range(0, len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        # print(statements)
        for j in range(0, len(statements)):
          try:
            if statements[j]['type'] != 'IfStatement':
              # print("here")
              continue
            else:
                if statements[j]['type'] == 'IfStatement' and statements[j]['condition']['left']['type'] == 'MemberAccess' and statements[j]['condition']['left']['memberName'] == 'gas':
                  print("Use of msg.gas is depracated! Use gasleft() in function: " + nodes[i]['name'] + '()')
                  flags.append("Use of msg.gas is depracated! Use gasleft() in function: " + nodes[i]['name'] + '()')
          except:
            # print("except:")
            continue
      except:
        pass
  except:
    pass
  
  # case 2: if msg.gas in require
  try:
    if len(requires) != 0:
      for key, value in requires.items():
        if 'msg.gas' in value[1]:
          print("Use of msg.gas is depracated! Use gasleft() in function: " + nodes[i]['name'] + '()')
          flags.append("Use of msg.gas is depracated! Use gasleft() in function: " +  nodes[i]['name'] + '()')
  except:
    pass
  if len(flags) != 0:
    detectors["deprecated-standards"] = flags
  else:
    detectors["deprecated-standards"] = None

    
# CUSTOM DETECTORS
def contract_summary(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = variable_handler(main.su['children'][index])

  print("\n---------- Contract summary for: ", name_of_the_contract + ' -----------')
  print("\nImports: ", list(main.suo.imports))
  print("\nPragmas: ", main.suo.pragmas[0]['value'])
  print("\nUser-Defined Variables: ", userDefined_member_data)
  print("\nPrimitive Variables: ", primitive_variable_data)
  print("\nFunctions: ", list(main.suo.contracts[name_of_the_contract].functions.keys()))
  print("\nFunction Data: ")
  pprint.pprint(function_data)
  print("\nFunction Member Info: ", function_member_data)


# UPDATED CONTROL FLOW
def control_flow(name_of_the_contract):
   
  control_flow = {}
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  #check if the contract is empty
  if len(nodes) == 0:
    return
  
  for i in range(0, len(nodes)):
    # print(len(nodes))
    if nodes[i]['type'] == 'StateVariableDeclaration' or nodes[i]['type'] == 'FunctionDefinition':

      if nodes[i]['type'] == 'StateVariableDeclaration':
        # print("here")
        control_flow_list = []

        state_var_name = nodes[i]['variables'][0]['name']
        # print(state_var_name)

        # handling arrays and 2D arrays
        if nodes[i]['initialValue'] != None:
          if 'expression' in nodes[i]['variables'][0].keys():
            try:
              if nodes[i]['variables'][0]['typeName']['baseTypeName']['type'] == 'ArrayTypeName':
                initialValue = 'two-dimenional-array'
              else:
                initialValue = 'array'
            except:
              if nodes[i]['variables'][0]['expression']['type'] == 'MemberAccess':
                initialValue = nodes[i]['variables'][0]['expression']['expression']['name'] + '.' +  nodes[i]['variables'][0]['expression']['memberName']
                # print(initialValue)
          else:
            expression = nodes[i]['variables'][0]['expression']
            datatype = nodes[i]['variables'][0]['typeName']['name']
            # print(datatype)
            initialValue = initialValue_handler(expression, datatype)
            # print(initialValue)

        elif nodes[i]['initialValue'] == None:
          # print("none")
          initialValue = None

        if state_var_name in control_flow.keys():
          newValue = control_flow.get(state_var_name)
          # print(newValue)
          newValue.append(initialValue)
          control_flow[state_var_name] = newValue
        else:
          # print("here")
          control_flow_list.append(initialValue)
          control_flow[state_var_name] = control_flow_list
           
      elif nodes[i]['type'] == 'FunctionDefinition':
        # print("here")
        name = nodes[i]['name']+'()'
        statements = nodes[i]['body']['statements']
        function_flow = {}
     
        try:
          for j in range(0, len(statements)):
            function_flow_list = []
            try:
            # for local variable initialization inside a function
              if 'initialValue' in statements[j].keys():
                var_name = statements[j]['variables'][0]['name']
                # print(var_name)
                if statements[j]['initialValue'] != None:
                  initialValue =  statements[j]['initialValue']['number']
                else:
                   initialValue = None
              
              # check if variable modification is due to simple assignment
              elif 'expression' in statements[j].keys() and statements[j]['expression']['type'] == 'BinaryOperation' and statements[j]['expression']['operator'] == '=':
                # print("here")
                var_name = statements[j]['expression']['left']['name']
                # print(var_name)
                try:
                  # in case of member access assignment
                  if statements[j]['expression']['right']['type'] == 'MemberAccess':
                    #  print("here")
                     initialValue = statements[j]['expression']['right']['expression']['name'] + "." + statements[j]['expression']['right']['memberName']
                  else:
                     x = 2/0
                except:
                  # print("here") 
                  if statements[j]['expression']['right']['type'] == 'BinaryOperation':
                    try:
                      initialValue = statements[j]['expression']['right']['left']['number'] + statements[j]['expression']['right']['operator'] + statements[j]['expression']['right']['right']['number']
                    except:          
                      initialValue = "Arithemtic Operation"              
                  # check if value modification is due to a function call
                  elif statements[j]['expression']['right']['type'] == "FunctionCall":
                    if statements[j]['expression']['right']['expression']['type'] == 'MemberAccess':
                        initialValue = "FunctionCall: " + statements[j]['expression']['right']['expression']['expression']['name'] + "." + statements[j]['expression']['right']['expression']['memberName'] + "()"
                    else:
                        initialValue = "FunctionCall: " + statements[j]['expression']['right']['expression']['name'] + "()"

                  elif statements[j]['expression']['type'] == 'BinaryOperation':
                    # print("here")
                    initialValue = statements[j]['expression']['left']['name'] + statements[j]['expression']['operator'] + statements[j]['expression']['right']['name']
                  else:
                    initialValue = statements[j]['expression']['right']['number']
            
              # check if variable modification is due to unary operation
              elif 'expression' in statements[j].keys() and statements[j]['expression']['type'] == 'UnaryOperation':
                # print("unary operation")
                var_name = statements[j]['expression']['main.subExpression']['name']
                initialValue = var_name + statements[j]['expression']['operator']
 
              else:
                continue # to skip the next statements as no variable modification is being done

              # check if state variable is being modified
              # print("herer")
              if var_name in control_flow.keys():
                newValue = control_flow.get(var_name)
                # print(newValue)
                newValue.append(initialValue)
                control_flow[var_name] = newValue

              # check if local variable is being modified 
              elif var_name in function_flow.keys():
                # print(initialValue)
                newValue = function_flow.get(var_name)
                newValue.append(initialValue)
                function_flow[var_name] = newValue
                control_flow[name] = function_flow

              else:
                # print("here")
                # print(initialValue)
                function_flow_list.append(initialValue)
                function_flow[var_name] = function_flow_list
                control_flow[name] = function_flow
            except:
               pass
        except:
           pass
      else:
         try:
            pass
         except:
            pass
  
  # print("\nControl Flow: ")
  # for k,v in control_flow.items():
  #   print("*", k + ": " , v)


  # external calls in functions 
  external_calls = {}
  calls_list = []
  for i in range(0, len(nodes)):
    if nodes[i]['type'] != 'FunctionDefinition':
      continue
    else:
      statements = nodes[i]['body']['statements']
      for j in range(0, len(statements)):    
        func_name = nodes[i]['name'] + "()"
        # print("\n",func_name)
        # print("\n\n", statements[j])
        try:
          if 'initialValue' in statements[j].keys() and statements[j]['initialValue']['type'] == 'FunctionCall':

            # print(statements[j]['variables'][0]['name'] + "=" + statements[j]['initialValue']['expression']['expression']['name'] + '.' + statements[j]['expression']['memberName'] )

            calls_list.append(statements[j]['variables'][0]['name'] + "=" + statements[j]['initialValue']['expression']['expression']['name'] + '.' + statements[j]['expression']['memberName'])
            external_calls[func_name] = calls_list

          elif statements[j]['expression']['type'] == "FunctionCall":
            # print("function call detected")
            calls_list.append( statements[j]['expression']['expression']['expression']['name'] + '.' + statements[j]['expression']['expression']['memberName'] + "()" )
            external_calls[func_name] = calls_list

          elif statements[j]['expression']['right']['type'] == 'FunctionCall':     
            calls_list.append(statements[j]['expression']['right']['expression']['expression']['name'] + '.' + statements[j]['expression']['right']['expression']['memberName'] + "()" )
            external_calls[func_name] = calls_list

          
        except:
          pass

  # print("\nExternal Calls in functions: ")
  # for k,v in external_calls.items():
  #   print("*", k + ": " , v)

  return control_flow, external_calls


def naming_convention(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  flags = []
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = variable_handler(main.su['children'][index])


  for key, value in primitive_variable_data.items():
    if ('l' in key or 'O' in key or 'I' in key) and len(key) == 1:
      runner.info += 1
      print(colored("\n[Informational] naming-convention. " + name_of_the_contract + '.' + key+ " uses '" + key + "'. Often indistinguishable from the numerals one and zero." , "green" ))
      runner.info += 1
      flags.append(name_of_the_contract + '.' + key+ " uses '" + key + "'. Often indistinguishable from the numerals one and zero.")

    if (key.islower() or key.isupper()) and len(key) > 8:
      print(colored("\n[Informational] naming-convention. " + name_of_the_contract + '.' + key+ " Use mixedCase." , "green" ))
      runner.info += 1
      flags.append(name_of_the_contract + '.' + key + "Use mixedCase.")

    # print(primitive_variable_data)
    if value[2] == True and not key.isupper():
      print(colored("\n[Informational] naming-convention. " + name_of_the_contract + '.' + key + " is a constant and should be named with all capital letters. " , "green"))
      runner.info += 1
      flags.append( name_of_the_contract + '.' + key + " is a constant and should be named with all capital letters. ")
      

  for key, value in function_member_data.items():
    for k,v in value.items():
      if ('l' in k or 'O' in k or 'I' in k) and len(k) == 1:
        print(colored("\n[Informational] naming-convention. " + name_of_the_contract + '.' + k + " uses '" + k + "'. Often indistinguishable from the numerals one and zero." , "green" ))
        runner.info += 1
        flags.append(name_of_the_contract + '.' + k + " uses '" + k + "'. Often indistinguishable from the numerals one and zero.")

      if (k.islower() or k.isupper()) and len(k) > 8:
        if k == "constructor":
          continue
        print(colored("\n[Informational] naming-convention. " + name_of_the_contract + '.' + key + '().' + k + " Use mixedCase." , "green" ))
        runner.info += 1
        flags.append(name_of_the_contract + '.' + key + '().' + k + " Use mixedCase.")

  for key, value in userDefined_member_data.items():
    if key.islower():
      print(colored("\n[Informational] naming-convention. " + key + " : is in small case. Please use CapWords style." , "green"))
      runner.info += 1
      flags.append(key + " : is in small case. Please use CapWords style." )

  for key, value in function_data.items():
    # print(key)
    if (key.islower() or key.isupper()) and len(key) >= 7:
      if key == "constructor":
        continue
      print(colored("\n[Informational] naming-convention. " + key + " : should use mixedCase style." , "green"))
      runner.info += 1
      flags.append(key + " : should use mixedCase style.")
  
  if name_of_the_contract[0].islower():
    print(colored("\n[Informational] naming-convention. Contract name should be in CapWords style." , "green"))
    runner.info += 1
    flags.append("Contract name should be in CapWords style.")

  events = event_handler(name_of_the_contract)
  for e in events:
    if e[0].islower():
      print(colored("\n[Informational] naming-convention. " + name_of_the_contract + '.' + e + "Event name should be in CapWords style." , "green"))
      runner.info += 1
      flags.append(name_of_the_contract + '.' + e + "Event name should be in CapWords style.")
  
  detectors["naming-conventions"] = flags
