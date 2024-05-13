import sys
sys.path.append('C:/Users/DELL/Documents/GitHub/mercury/')
from ImmuneLite_v1 import informational, runner
import pprint
import main
from termcolor import colored


# ONLY SPECIFIC TO PRAGMA VERSION 0.4.22
def multiple_constructors(name_of_the_contract):
  try:
     
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    # n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
    # pprint.pprint(constrcutor_data)
    informational.flags = []
    if len(constrcutor_data) > 1:
      print(colored("\n[High] multiple-constructors: Detected multiple constructor definitions in the same contract (using new and old schemes.\n" , "red"))
      runner.high += 1
      informational.flags.append("Detected multiple constructor definitions in the same contract (using new and old schemes")
      informational.detectors["multiple_constructors"] = informational.flags
  except:
    informational.detectors["multiple_constructors"] = None

def uninitialized_state(name_of_the_contract):
  try:
        n, name_of_contracts = runner.name_of_contracts_function(main.su)
        # print(name_of_contracts.index(name_of_the_contract))
        index = name_of_contracts.index(name_of_the_contract) + n
        nodes = main.su['children'][index]['subNodes']
        userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constructor_data, requires = informational.variable_handler(main.su['children'][index])
        # pprint.pprint(primitive_variable_data)
        informational.flags = []

        #primitive will also contain array. We dont want to run this loop on arrays.
        try:
          for key, value in primitive_variable_data.items():
              # print(key)
              if value[0] == 'array':
                  if value[4] == True and value[2] == 'uninitialized': 
                      flag = 0
                      for i in range(0, len(nodes)):
                        # print(key)
                        try:
                          statements = nodes[i]['body']['statements']
                          stmt_str = str(statements)
                          # print(stmt_str)
                          if key in stmt_str:
                            for j in range(0, len(statements)):
                              if statements[j]['type'] != 'ExpressionStatement':
                                flag = 0
                              else:
                                # print("else running")
                                if statements[j]['expression']['type'] == 'BinaryOperation':
                                  # print(key)
                                  if key == statements[j]['expression']['left']['base']['name']:
                                    flag = 1
                                else:
                                  flag = 0
                        except:
                          pass
                  else:
                    flag = 1
              else:
                  temp = 0
                  if value[3] == True and value[1] == 'uninitialized':
                      flag = 0               
                      for i in range(0, len(nodes)):
                        # print(key)
                        if temp == 1:
                          break
                        try:
                          statements = nodes[i]['body']['statements']
                          stmt_str = str(statements)
                          # print("\n",stmt_str)
                          if key in stmt_str:
                            for j in range(0, len(statements)):
                              if statements[j]['type'] != 'ExpressionStatement':
                                # print("herre")
                                flag = 0
                              else:
                                # print("else running")
                                if statements[j]['expression']['type'] == 'BinaryOperation':
                                  # print("///////////", key)
                                  if key == statements[j]['expression']['left']['name']:
                                    flag = 1
                                    temp = 1
                                    # print("matched")
                                    break
                                elif statements[j]['expression']['type'] == 'UnaryOperation':
                                  if key == statements[j]['expression']['main.subExpression']['name']:
                                    flag = 1
                                    temp = 1
                                    break
                                else:
                                  # print("herrrrrrre")
                                  flag = 0
                        except:
                          pass
                  else:
                    flag = 1

              if flag == 0:
                print(colored("[High] uninitialized-state-variable: ", "red") + colored(str(name_of_the_contract) + "." + str(key), "red") + colored(" is not initialized." , "red"))   
                runner.high +=1 
                informational.flags.append(name_of_the_contract + "." + str(key))
                informational.detectors["uninitialized_state"] = informational.flags
        except:
            informational.detectors["uninitialized_state"] = None
  except :
    informational.detectors["uninitialized_state"] = None

def uninitialized_local(name_of_the_contract):
  try:
     
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    # n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    # print(name_of_contracts)
    userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
    # pprint.pprint(function_member_data)
    # print(function_member_data.keys())
    # pprint.pprint(function_data)
    informational.flags = []

    assembly_assignment = {}
    for i in range(0, len(nodes)):
      try:
          statements = nodes[i]['body']['statements']
          for j in range(0, len(statements)):
            try:
              # print(statements[j]['body']['type'])
              if statements[j]['body']['type'] == 'AssemblyBlock':
                operations = statements[j]['body']['operations']
                for o in range(0, len(operations)):
                  var = statements[j]['body']['operations'][o]['names'][0]['name']
                  oper_str = str(operations[o])
                  if 'AssemblyAssignment' in oper_str:
                    assembly_assignment[var] = "Yes"
            except:
              pass
      except:
        pass
    try:
      for key, value in function_member_data.items():
        # print("\n\nKey:   " + key)
        for k,v in value.items():
          try:
            if v[1] == 'uninitialized' :
              if assembly_assignment[k] == "Yes":
                continue

              print( colored("\n[Medium] uninitialized-local: " + name_of_the_contract + '.' + key + '.' + k + " is a local variable never initialized." , "yellow"))
              runner.medium +=1
              informational.flags.append(name_of_the_contract + '.' + key + '.' + k )
              informational.detectors["uninitialized-local"] = informational.flags
          except:
                          informational.detectors["uninitialized-local"] = None
    except:
      informational.detectors["uninitialized-local"] = None
  except:
    informational.detectors["uninitialized-local"] = None

def shadowing_local(name_of_the_contract):
  try:
     
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    informational.flags = []

    userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constructor_data, requires = informational.variable_handler(
        main.su['children'][index])
    reused_names = []
    # print(primitive_variable_data)

    #even if the dictionary is empty, it wont return an error and it will be blank 
    variable_names = list(primitive_variable_data.keys())
    # print(variable_names)

    var_dict = {}
    for key, value in function_member_data.items():
      for k, v in value.items():
        var_dict[k] = len(v)
    
    # print(var_dict)

    for var in variable_names:
      for i in range(0, len(nodes)):
        try:
          statements = nodes[i]['body']['statements']
          for j in range(0, len(statements)):
            stmt_str = str(statements)
            if var in stmt_str:
              # print("yes")
              if var in var_dict and var_dict[var] == 3:
                reused_names.append(var)
                print(colored("\n[Low] shadowing-local. " + name_of_the_contract + '.' + nodes[i]['name'] + "()." + var + " shadows " + name_of_the_contract + '.' + k , "green"))
                runner.low +=1
                informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + "()." + var + " shadows " + name_of_the_contract + '.' + k )
                break
            informational.detectors["shadowing-local"] = informational.flags
        except:
          informational.detectors["shadowing-local"] = None
      
    # print(reused_names)
    return reused_names
  except Exception as e:
    print(colored("\nAn error occurred in impact.py in function shadowing while extracting remain.sused variable names (Line 48-74): ",'green'),colored(e,'red'))

def calls_loop(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []

  for i in range(0, len(nodes)):
      try:
        x = nodes[i]['body']['statements']
        # pprint.pprint(x)
        for j in range(0,len(x)):
          if  x[j]['type'] == 'ForStatement' or x[j]['type'] == 'WhileStatement' or x[j]['type'] == 'DoWhileStatement':
            for l in range(0,len(x[j]['body']['statements'])):  # for/while block
              for_str = str(x[j]['body']['statements'][l])
              # print(for_str)
              if 'FunctionCall' in for_str:
                  name = x[j]['body']['statements'][l]['expression']['expression']['memberName']
                  # print(name)
                  print(colored("\n[Low] calls-loop. " + name_of_the_contract + '.' + nodes[i]['name'] + "() has external calls inside a loop: " + name + '()', "green"))
                  runner.low += 1
                  informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + "() has external calls inside a loop: " + name + '()')
            informational.detectors["calls-loop"] = informational.flags
          else:
            x = 2/0
      except:
        # for unchecked block
        # print("here")
        try:
          x = nodes[i]['body']['statements']  #function body
          for k in range(0, len(x)):
            try:
              y = x[k]['body']['statements']   #unchecked body
              for j in range(0,len(y)):
                # pprint.pprint(y)
                if  y[j]['type'] == 'ForStatement' or y[j]['type'] == 'WhileStatement' or y[j]['type'] == 'DoWhileStatement':
                  for h in range(0, len(y[j]['body']['statements'])):  # for/while block
                    for_str = str(y[j]['body']['statements'][h])
                    if 'FunctionCall' in for_str:
                      name = y[j]['body']['statements'][h]['expression']['expression']['memberName']
                      # print(name)
                      print(colored("\n[Low] calls-loop. " + name_of_the_contract + '.' + nodes[i]['name'] + "() has external calls inside a loop: " + name + '()' , "green"))
                      runner.low += 1
                      informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + "()")
                      informational.detectors["calls-loop"] = informational.flags
            except:
              continue
        except:
          informational.detectors["calls-loop"] = None
      
def boolean_cst(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []

  try:
    for i in range(0, len(nodes)):
      if nodes[i]['type'] != 'FunctionDefinition':
        continue
      else:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          if statements[j]['type'] == 'IfStatement' or statements[j]['type'] == 'WhileStatement':

            # case 1: if (true) or if (false) -- same will be the case with while statements
            if statements[j]['condition']['type'] == 'BooleanLiteral':
              print(colored("\n[Medium] boolean-cst. ", "yellow") + colored(str(name_of_the_contract) + "." + str(nodes[i]['name']) , "yellow") + colored(" uses a Boolean constant improperly.", "yellow"))
              runner.medium +=1
              informational.flags.append(name_of_the_contract + "." + str(nodes[i]['name']) )

            # case 2: if (b || true) or (true || b) [b is boolean] 
            if 'value' in statements[j]['condition']['right'].keys() and statements[j]['condition']['right']['value'] == False or statements[j]['condition']['right']['value'] == True:
              # print(statements[j]['condition']['right']['value'])
              print(colored("\n[Medium] boolean-cst. ", "yellow") + colored(str(name_of_the_contract) + "." + str(nodes[i]['name']) , "yellow") + colored(" uses a Boolean constant improperly.", "yellow"))
              runner.medium +=1
              informational.flags.append(name_of_the_contract + "." + str(nodes[i]['name']) )

            elif 'value' in statements[j]['condition']['left'].keys() and statements[j]['condition']['left']['value'] == False or statements[j]['condition']['right']['value'] == True:
              print(colored("\n[Medium] boolean-cst. ", "yellow") + colored(str(name_of_the_contract) + "." + str(nodes[i]['name']) , "yellow") + colored(" uses a Boolean constant improperly.", "yellow"))
              runner.medium +=1
              informational.flags.append(name_of_the_contract + "." + str(nodes[i]['name']) )

          elif statements[j]['type'] == 'ExpressionStatement' and statements[j]['expression']['right']['type'] == 'BinaryOperation':
              dict_str = str(statements[j]['expression'])
              # print(dict_str)
              if 'BooleanLiteral' in dict_str:
                print(colored("\n[Medium] boolean-cst. ", "yellow") + colored(str(name_of_the_contract) + "." + str(nodes[i]['name']) , "yellow") + colored(" uses a Boolean constant improperly.", "yellow"))
                runner.medium +=1
                informational.flags.append(name_of_the_contract + "." + str(nodes[i]['name']) )
          
          elif 'initialValue' in statements[j].keys():
            if statements[j]['variables'][0]['typeName']['name'] == 'bool' and statements[j]['initialValue']['type'] == 'BinaryOperation':
              dict_str = str(statements[j]['initialValue'])
              # print(dict_str)
              if 'BooleanLiteral' in dict_str:
                print(colored("\n[Medium] boolean-cst. ", "yellow") + colored(str(name_of_the_contract) + "." + str(nodes[i]['name']) , "yellow") + colored(" uses a Boolean constant improperly.", "yellow"))
                informational.flags.append(name_of_the_contract + "." + str(nodes[i]['name']) )
                runner.medium +=1

          else:
            dict_str = str(statements[j])
            # pprint.pprint(statements[j])
            if 'BooleanLiteral' in dict_str:
              if statements[j]['type'] == 'BinaryOperation' or statements[j]['components'][0]['type']:
                print(colored("\n[Medium] boolean-cst. ", "yellow") + colored(str(name_of_the_contract) + "." + str(nodes[i]['name']) , "yellow") + colored(" uses a Boolean constant improperly.", "yellow"))
                informational.flags.append(name_of_the_contract + "." + str(nodes[i]['name']) )
                runner.medium +=1
  except:
    pass

  if len(informational.flags) != 0:
    informational.detectors["boolean-cst"] = informational.flags
  else:
    informational.detectors["boolean-cst"] = None

def divide_before_multiply(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  su = main.su['children'][index]['subNodes']
  informational.flags = []

  for i in su:
    # pprint.pprint(i['initialValue'])
    operator_list = []
    try:
      iv = i['initialValue']
      # print(iv) 
      while iv['type']:
        if iv['type'] == 'BinaryOperation':
          operator_list.append(iv['operator'])
        elif iv['type'] == 'TupleExpression':
          pass
        try:
              iv = iv['left']
        except:
              iv = iv['components'][0]
    except:
      #code will be executed here as iv here is second last left 
      try:
        sorted_operator_list = []
        l = len(operator_list)-1
        while l>-1:
          sorted_operator_list.append(operator_list[l])
          l-=1
        # pprint.pprint(sorted_operator_list)
        divide = False
        for k in sorted_operator_list:
          if k == '/':
            divide = True
          if k == '*' and divide:
            print(colored("\n[Medium] divide-before-multiply. ","yellow") + colored(str(name_of_the_contract) + '.' + str(i['name']) + "() performs a multiplication on the result of a division", "yellow"))
            runner.medium +=1
            informational.flags.append(name_of_the_contract + '.' + str(i['name']) + "() ")
            informational.detectors["divide-before-multiply"] = informational.flags
      except:
        informational.detectors["divide-before-multiply"] = None
      
    try:
      # for functions containing divide before multiply
      if i['type'] == 'FunctionDefinition':
        for j in i['body']['statements']:
          try:
            if 'initialValue' in j.keys():
              try:
                iv = j['initialValue']
                # print(iv)
                operator_list = []
                while iv['type']:
                  if iv['type'] == 'BinaryOperation':
                    operator_list.append(iv['operator'])
                  elif iv['type'] == 'TupleExpression':
                    pass
                  try:
                        iv = iv['left']
                  except:
                        iv = iv['components'][0]
              except:
                #code will be executed here as iv here is second last left 
                sorted_operator_list = []
                l = len(operator_list)-1
                while l>-1:
                  sorted_operator_list.append(operator_list[l])
                  l-=1
                # pprint.pprint(sorted_operator_list)
                divide = False
                for k in sorted_operator_list:
                  if k == '/':
                    divide = True
                  if k == '*' and divide:
                    print(colored("\n[Medium] divide-before-multiply. ","yellow") + colored(str(name_of_the_contract) + '.' + str(i['name']) + "() performs a multiplication of the result on a division", "yellow"))
                    runner.medium +=1
                    informational.flags.append(name_of_the_contract + '.' + str(i['name']) + "()" )
            else:
              x = 2/0
          except:
            if 'initialValue' not in j.keys():
              try:
                if j['expression']['right']['type'] == 'BinaryOperation':
                  try:
                    iv = j['expression']['right']
                    # print(iv)
                    operator_list = []
                    while iv['type']:
                      if iv['type'] == 'BinaryOperation':
                        operator_list.append(iv['operator'])
                      elif iv['type'] == 'TupleExpression':
                        pass
                      try:
                            iv = iv['left']
                      except:
                            iv = iv['components'][0]
                  except:
                    #code will be executed here as iv here is second last left 
                    sorted_operator_list = []
                    l = len(operator_list)-1
                    while l>-1:
                      sorted_operator_list.append(operator_list[l])
                      l-=1
                    # pprint.pprint(sorted_operator_list)
                    divide = False
                    for k in sorted_operator_list:
                      if k == '/':
                        divide = True
                      if k == '*' and divide:
                        print(colored("\n[Medium] divide-before-multiply. ","yellow") + colored(str(name_of_the_contract) + '.' + str(i['name']) + "() performs a multiplication on the result of a division", "yellow"))
                        runner.medium +=1
                        informational.flags.append(name_of_the_contract + '.' + str(i['name']) + "()" )
                        informational.detectors["divide-before-multiply"] = informational.flags
              except:
                informational.detectors["divide-before-multiply"] = None
    except:
      informational.detectors["divide-before-multiply"] = None

def void_cst(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  informational.flags = []
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data , constructor_data, requires = informational.variable_handler (main.su['children'][index])
  # pprint.pprint(constructor_data)
    
  try: 
    for key,value in constructor_data.items():
      if key == "constructor":
        constructor_name = value[2][0]['name']
        # print("1 constructor: " + constructor_name + "\n")
  
    inheritance = runner.inheritance_handler(name_of_the_contract)
    # print(inheritance)
  
    for i in inheritance:
      if i == constructor_name:
        # print(i, j) 
        n, new_contract = runner.name_of_contracts_function()
        index2 = new_contract.index(constructor_name) + 1
    # print(index2)
   
    userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler (main.su['children'][index2])
    # print("this", constructor_data)
  
    if len(constructor_data) == 0:
       print(colored("\n[Low] vois-cst. " + name_of_the_contract + '.' + constructor_name + '() is a void constructor' , "green"))
       runner.low += 1
       informational.detectors["void-cst"] = [name_of_the_contract + '.' + constructor_name + '()']
  except:
    informational.detectors["void-cst"] = None
            
def missing_inheritance(name_of_the_contract):
  # print(name_of_the_contract)
   
  informational.flags = []
  try:    
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    inheritance = runner.inheritance_handler(name_of_the_contract)
    # print(inheritance)
  
    userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data_main, constructor_data, requires  = informational.variable_handler (main.su['children'][index])
    keys = list(function_data_main.keys())
    # print("Keys: ", keys)
    count = 1
    for n in count(name_of_contracts):
      count += 1
      userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler (main.su['children'][index+count])
      keys2 = list(function_data.keys())
  
      for key, value in function_data_main.items():
        for k,v in value.items():
          if k in keys and key not in inheritance:
            print(colored("\n[Low] missing-inheritence. " + name_of_the_contract + '.' + k + "() can be inherited from " + key , "green"))
            runner.low +=1
            informational.flags.append(name_of_the_contract + '.' + k + "() can be inherited from " + key )
      informational.detectors["missing-inheritance"] = informational.flags
  except:
    informational.detectors["missing-inheritance"] = None

def msg_value(name_of_the_contract):
    
   n, name_of_contracts = runner.name_of_contracts_function(main.su)
   index = name_of_contracts.index(name_of_the_contract) + n
   nodes = main.su['children'][index]['subNodes']
   informational.flags = []
   # pprint.pprint(nodes)
   for i in range(0,len(nodes)):
    try:
      for j in range(0, len(nodes[i]['body']['statements'])):
        function_name = nodes[i]['name']
        try:
          if nodes[i]['body']['statements'][j]['type'] == 'ForStatement':
            for_str = str(nodes[i]['body']['statements'][j]['body']['statements'])
            if 'msg' in for_str and 'value' in for_str:
              print(colored("\n[High] msg.value-in-loop. " + name_of_the_contract + '.' + function_name + '() uses msg.value in loop.' , "red"))
              runner.high += 1
              informational.flags.append(name_of_the_contract + '.' + function_name + '()')
          informational.detectors["msg.value-in-loop"] = informational.flags
        except:
          informational.detectors["msg.value-in-loop"] = None
    except:
      informational.detectors["msg.value-in-loop"] = None
      # print("except is running")
  
def suicidal(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  # pprint.pprint(nodes)
  informational.flags = []

  for i in range(0,len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0,len(statements)):
        try:
          if j == 0 and len(statements) == 2 and statements[j]['expression']['expression']['name'] == 'require' and statements[1]['expression']['expression']['name'] == 'selfdestruct':
            break
          else: #intentional error
            x = 10/0 
        except:
          try:
            if j == 1 and statements[1]['expression']['expression']['name'] == 'selfdestruct' and len(statements) == 2:
              print(colored("\n[High] main.suicidal. " + name_of_the_contract + '.' + nodes[i]['name'] + '() allows anyone to destruct the contract' , "red"))
              runner.high += 1
              informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '() allows anyone to destruct the contract')
              informational.detectors["main.suicidal"] = informational.flags
              return nodes[i]['name']
            else: #intentional error
              x = 10/0 
          except:
            try:
              if statements[j]['expression']['expression']['name'] == 'selfdestruct':
                print(colored("\n[High] main.suicidal. " + name_of_the_contract + '.' + nodes[i]['name'] + '() allows anyone to destruct the contract' , "red"))
                runner.high += 1
                informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '() allows anyone to destruct the contract')
                informational.detectors["main.suicidal"] = informational.flags
                return nodes[i]['name']
            except:
              continue
    except:
      informational.detectors["main.suicidal"] = None

def controlled_array_length(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  # pprint.pprint(nodes)
  informational.flags = []

  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data, constrcutor_data, requires  = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(primitive_variable_data)

  for i in range(0,len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0,len(statements)):
        try:
          if statements[j]['expression']['left']['memberName'] == 'length':
            name = statements[j]['expression']['left']['expression']['name']
            # print(name)
            if name in primitive_variable_data and primitive_variable_data[name][0] == 'array':
              print(colored("\n[High] controlled-array-length. " + name_of_the_contract + " contract sets array length with a user-controlled value. " + name + ".length is set." , "red"))
              informational.flags.append(name_of_the_contract + " contract sets array length with a user-controlled value. " + name + ".length is set.")
              informational.detectors["controlled-array-length"] = informational.flags
              runner.high += 1
        except:
          informational.detectors["controlled-array-length"] = None
    except:
      informational.detectors["controlled-array-length"] = None

def txorigin(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  # pprint.pprint(nodes)
  informational.flags = []

  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler(main.su['children'][index])
  # print(primitive_variable_data)
  
  for i in range(0,len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0,len(statements)):
        try:
          expression = statements[j]['expression']
          name = expression['arguments'][0]['left']['expression']['name']
          member_name = expression['arguments'][0]['left']['memberName']
          # pprint.pprint(member_name)
          try:
            if expression['expression']['name'] == 'require' and name == 'tx' and member_name == 'origin':
              variable_name = expression['arguments'][0]['right']['name']
              # print(variable_name)  
              
              if variable_name in primitive_variable_data and primitive_variable_data[variable_name][1] == 'msg.sender':
                print(colored("\n[Medium] dangerous usage of tx-origin. " + name_of_the_contract + '.' + nodes[i]['name'] + '() uses tx.origin for authorization.' , "yellow"))
                informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
                runner.medium += 1           
          except:
            if expression['arguments'][0]['right']['expression']['name'] == 'msg' and expression['arguments'][0]['right']['memberName'] == 'sender':
              print(colored("\n[Medium] dangerous usage of tx-origin. " + name_of_the_contract + '.' + nodes[i]['name'] + '() uses tx.origin for authorization.' , "yellow"))
              informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
              runner.medium += 1 
        except:
          stmt = str(statements[j])
          if 'tx' in stmt and 'origin' in stmt:
            print(colored("\n[Medium] dangerous usage of tx-origin. " + name_of_the_contract + '.' + nodes[i]['name'] + '() uses tx.origin for authorization.' , "yellow"))
            informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
            runner.medium += 1
        informational.detectors["tx-origin"] = informational.flags
    except:
              informational.detectors["tx-origin"] = None

def incorrect_shift(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []

  for i in range(0,len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0,len(statements)):
        try:
          if statements[j]['type'] == 'InLineAssemblyStatement':
            # print("yes")
            operations = statements[j]['body']['operations']
            for k in range(0, len(operations)):
              try:
                expression = statements[j]['body']['operations'][k]['expression']
                if expression['functionName'] == "shr" or expression['functionName'] == "shl":
                  if 'functionName' in expression['arguments'][0] and 'value' in expression['arguments'][1]:
                    print(colored("\n[High] incorrect-shift. " + name_of_the_contract + '.' + nodes[i]['name'] + '() contains an incorrect shift operation' , "red"))
                    runner.high += 1
                    informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + '()')
                informational.detectors["incorrect-shift"] = informational.flags
              except:
                informational.detectors["incorrect-shift"] = None
        except:
          informational.detectors["incorrect-shift"] = None
    except:
      informational.detectors["incorrect-shift"] = None

def controlled_delegatecall(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []
  for i in range(0,len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0,len(statements)):
        # pprint.pprint(statements[j]) 
        try:
          expression = statements[j]['expression']
          if expression['expression']['memberName'] == 'delegatecall' and expression['arguments'][0]['type'] == 'Identifier':
            var_name = expression['arguments'][0]['name']
            # print(var_name)
            parameters = nodes[i]['parameters']['parameters']
            # pprint.pprint(parameters)        
        except:
          continue

        for parameter in parameters:
          if parameter['name'] == var_name:
            print(colored("\n[High] controlled-delegatecall. " + name_of_the_contract + '.' + nodes[i]['name'] + "() uses delegatecall to input-controlled function id" , "red"))
            informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'] + "()")
            runner.high += 1
        informational.detectors["controlled-delegatecall"] = informational.flags
    except:
        informational.detectors["controlled-delegatecall"] = None
        
def delegate_call_in_loop(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []

  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constructor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(function_member_data)

  for i in range(0,len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0,len(statements)):
        try:
          for k in range(0,len(statements[j]['body']['statements'])):
            try:
              exp = statements[j]['body']['statements'][k]['expression']['expression']
              if exp['memberName'] == 'delegatecall':
                # print("delegateCall() found inside loop")
                arg = statements[j]['body']['statements'][k]['expression']['arguments']
                try:
                  if arg[0]['expression']['memberName'] == 'encodeWithSignature':
                    func_name = arg[0]['arguments'][0]['value'].split('(')
                    if function_data[func_name[0]][6] == "payable":
                      # print(type(nodes[i]['name']))
                      print(colored("\n[High] delegatecall-inside-loop. " + name_of_the_contract + '.' + func_name[0] + '() has delegatecall inside a loop in payable function' , "red"))
                      informational.flags.append(name_of_the_contract + '.' + func_name[0] + '()')
                      runner.high += 1
                except:
                  if arg[0]['type'] == "FunctionCall":
                    func_name = arg[0]['expression']['name']
                    if function_data[func_name][6] == 'payable':
                      print(colored("\n[High] delegatecall-inside-loop. " + name_of_the_contract + '.' + func_name + '() has delegatecall inside a loop in payable function' , "red"))   
                      informational.flags.append(name_of_the_contract + '.' + func_name[0] + '()')
                      runner.high += 1
              informational.detectors["delegatecall-inside-loop"] = informational.flags
            except:
              continue
        except:
          continue
    except:
      informational.detectors["delegatecall-inside-loop"] = None

def storage_array(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(function_member_data)
  for i in range(0,len(nodes)):
    for key,value in function_member_data.items():
      for k,v in value.items():
        if "array" in v and 'signed' in v:
          print("Signed storage array: " + str(key) + " array name: " + str(k))
          informational.detectors["signed-array"] = [str(key) + "." + str(k)]
        else:
          informational.detectors["signed-array"] = None

def abiencoderv2_array(name_of_the_contract):
  # print("here")
   
  try:
    n, name_of_contracts = runner.name_of_contracts_function(main.su)
    index = name_of_contracts.index(name_of_the_contract) + n
    nodes = main.su['children'][index]['subNodes']
    userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
    # pprint.pprint(primitive_variable_data)
    # pprint.pprint(function_member_data)
    informational.flags = []

    for i in range(0,len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0,len(statements)):
          try:
            if statements[j]['initialValue']['type'] == 'FunctionCall' and statements[j]['initialValue']['expression']['memberName'] == 'encode':
              var_name = statements[j]['initialValue']['arguments'][0]['name']

              #now check if this variable name is a two-dimensional array or not
              if primitive_variable_data[var_name][0] == 'two-dimensional array':
                print(colored("\n[High] abiencoderv2-array. " + name_of_the_contract + '.' + var_name + " is a two-dimensional array passed to abi.encoder in " + name_of_the_contract + '.' + nodes[i]['name'] + '()' , "red"))
                informational.flags.append(name_of_the_contract + '.' + var_name + " is a two-dimensional array passed to abi.encoder in " + name_of_the_contract + '.' + nodes[i]['name'] + '()')
                informational.detectors["abiencoderv2-array"] = informational.flags
                runner.high += 1
              else:
                informational.detectors["abiencoderv2-array"] = None
          except:
            continue
      except:
        informational.detectors["abiencoderv2-array"] = None
  except:
    # print("here")
    informational.detectors["abiencoderv2-array"] = None

def incorrect_modifier(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []

  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constrcutor_data, requires = informational.variable_handler(main.su['children'][index])

  for i in range(0, len(nodes)):
    try:
      if nodes[i]['type'] != 'ModifierDefinition':
        # print(nodes[i]['name'])
        continue
      else:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          # pprint.pprint(statements[j])

          # case 1: if _; is inside if
          if statements[j]['type'] == 'IfStatement':
            if_str = str(statements[j])
            if '_' in if_str:
              print(colored("\n[Low] incorrect-modifier. " + name_of_the_contract + '.' + nodes[i]['name'] + " doesn't always execute _; or revertReference. " , "green" ))
              runner.low += 1
              informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'])
          
          #case 2: if _; is the first statement
          if j == 0 and statements[j]['expression']['name'] == '_':
            print(colored("\n[Low] incorrect-modifier. " + name_of_the_contract + '.' + nodes[i]['name'] + " always executed _; without checking the condition. " , "green" ))
            runner.low += 1
            informational.flags.append(name_of_the_contract + '.' + nodes[i]['name'])
        informational.detectors["incorrect-modifier"]  = informational.flags
    except:
      informational.detectors["incorrect-modifier"] = None

def shadowing_builtin(name_of_the_contract):
   
  informational.flags = []
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data , constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
  reserved_keywords = ['abstract', 'assert', 'after', 'alias', 'apply', 'auto', 'case', 'catch', 'copyof', 'default', 'define', 'final', 'immutable', 'implements', 'in', 'inline', 'let', 'macro', 'match', 'mutable', 'now' , 'null', 'of', 'override', 'partial', 'promise', 'reference', 'relocatable', 'sealed', 'sizeof', 'static', 'main.supports', 'switch', 'try', 'typedef', 'typeof', 'unchecked', 'byte', 'var']

  shadowed = []
  # print(primitive_variable_data,function_member_data,function_data)
  try:
    for i in primitive_variable_data:
      if i.lower() in reserved_keywords:
        shadowed.append(i)

    for key,value in function_member_data.items():
      if key.lower() in reserved_keywords:
        shadowed.append(key)
      for j in value:
        if j.lower() in reserved_keywords:
          shadowed.append(j)

    for i in function_data :
      if i.lower() in reserved_keywords:
        shadowed.append(i)

    if len(shadowed) != 0:
      for i in shadowed:
        print(colored("\n[Low] shadowing-builtin. " + name_of_the_contract + '.' + i + " shadows built-in symbol" , "green"))
        runner.low += 1
        informational.flags.append( name_of_the_contract + '.' + i)
        informational.detectors["shadowing-builtin"] = informational.flags
  except:
    informational.detectors["shadowing-builtin"] = None

def weak_prng(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  for i in range(0, len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0,len(statements)):
        # print(len(statements))
        stmt_str = str(statements[j])
        if ('timestamp' in stmt_str or 'blockhash' in stmt_str or 'now' in stmt_str) and '%' in stmt_str:
          print(colored("\n[High] weak-prng. " + name_of_the_contract + '.' + nodes[i]['name'] + '() uses a weak PRNG.' , "red"))
          informational.detectors["weak_prng"] = [name_of_the_contract + '.' + nodes[i]['name'] + '()']
          runner.high += 1
    except:
      pass

def locked_ether(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  informational.flags = []
  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data, constrcutor_data, requires  = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(primitive_variable_data)
  # pprint.pprint(function_data)

  #to check if payable is there in the contract
  isPayableThere = 0
  for i in range(0, len(nodes)):
    try:
      # print([nodes[i]['name']])
      # print(function_data[nodes[i]['name']][6])
      if function_data[nodes[i]['name']][6] == 'payable':
        isPayableThere = 1
        break 
      elif primitive_variable_data[nodes[i]['variables']['name']][2] == 'payable':
        isPayableThere = 1
        break
    except:
      pass

  # print(isPayableThere)
  #to check if withdrawl function is present
  isWithdrawThere = 0
  try:
    if isPayableThere:
      for i in range(0, len(nodes)):
        try:
          # print(nodes[i]['name'])
          statements = nodes[i]['body']['statements']
          for j in range(0, len(statements)):
            try:
              stmt_str =str(statements[j])
          
              if 'transfer' in stmt_str or 'transferFrom' in stmt_str:
                isWithdrawThere = 1
            except:
              continue
        except:
          continue

    if isWithdrawThere == 0 and isPayableThere == 1:
      print(colored("\n[Medium] locked-ether. Contract locking ether found: \n" + "\tContract " + name_of_the_contract + " has payable functions \n" + "\t-"+ name_of_the_contract + '.' + nodes[i]['name'] + "()\n" + "\tBut does not have a function to withdraw ether" , "yellow"))
      runner.medium += 1
      informational.detectors["locked-ether"] = [name_of_the_contract + '.' + nodes[i]['name'] + "()"]
  except:
    informational.detectors["locked-ether"] = None

def mapping_deletion(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data, constrcutor_data, requires  = informational.variable_handler(main.su['children'][index])
  #check if a struct contains a mapping
  informational.flags = []

  l = []
  try:
    for key,value in userDefined_member_data.items():
      for k,v in value.items():
        if 'Mapping' in v:
          l.append(key)
    # print(l)
  except:
      pass

  #now check if deletion is performed
  for i in range(0, len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0, len(statements)):
        try:
          if statements[j]['expression']['operator'] == 'delete': 
            
            if len(statements[j]['expression']['main.subExpression']) == 3 and statements[j]['expression']['main.subExpression']['type'] == 'IndexAccess': #deletion is performed on a mapping
              main.subExpression = statements[j]['expression']['main.subExpression']['base']['name']
              
              #check if that mapping contains a struct
              if primitive_variable_data[main.subExpression][0] == 'Mapping' and 'struct' in primitive_variable_data[main.subExpression][1][1]:
                struct_name = primitive_variable_data[main.subExpression][1][1].split(": ")[1]
                if struct_name in l:
                  print(colored("\n[Medium] mapping-deletion. " + name_of_the_contract + '.' + nodes[i]['name'] + '() deletes ' + name_of_the_contract + '.' + struct_name + " which contains a mapping" , "yellow"))
                  runner.medium += 1
                  informational.flags.append("struct_name")
              informational.detectors["mapping-deletion"] = informational.flags

            #when there is direct deletion of a struct containing a mapping
            elif len(statements[j]['expression']['main.subExpression']) == 2 and statements[j]['expression']['type'] == 'UnaryOperation':
              var_name = statements[j]['expression']['main.subExpression']['name']
              if var_name in userDefined_member_data and var_name in l:
                print(colored("\n[Medium] mapping-deletion. " + name_of_the_contract + '.' + nodes[i]['name'] + '() deletes ' + name_of_the_contract + '.' + var_name + "which contains a mapping" , "yellow"))
                runner.medium += 1
                informational.flags.append("mapping-deletion")
              informational.detectors["mapping-deletion"] = informational.flags
        except:
          informational.detectors["mapping-deletion"] = None
    except:
      informational.detectors["mapping-deletion"] = None


def public_mappings_nested(name_of_the_contract):
  informational.flags = []
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  #check solidity version first, if it is less than 0.5.0 ---> check nested mappings
  if float(main.pragma_value.split('0.')[1])> 5.0: 
    pass
  else:
    userDefined_member_data, primitive_variable_data, function_member_data,constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler(main.su['children'][index])

    for key,value in primitive_variable_data.items():
      try:
        if 'Mapping' in value[0] and primitive_variable_data[key][5] == 'public' and 'struct' in value[1][1]:
          structName = value[1][1].split(": ")[1]
          # print(userDefined_member_data[structName])
          for k,v in userDefined_member_data[structName].items():
            # print(v)
            if 'struct' in v[0]:
              print("\nNested structure present inside public mapping!")
              runner.info += 1
              informational.detectors["public_mappings_nested"] = ["Nested structure present inside public mapping"]
      except:
        informational.detectors["public_mappings_nested"] = None
        
def unused_return(name_of_the_contract):
   
  informational.flags = []
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(function_member_data)

  interfaces = runner.interfaces()
  # pprint.pprint(interfaces)
  
  for i in nodes:
    try:
      statements = i['body']['statements']
      for j in statements:
        return_val = ""
        try:
          if j['expression']['type'] == 'FunctionCall':
            if j['expression']['expression']['type'] == 'MemberAccess':
              func_name = j['expression']['expression']['memberName']

              #now we will check it's an interface
              try:
                interface_name = j['expression']['expression']['expression']['expression']['name']
                if interface_name:
                  interface_functions = list(interfaces[interface_name].keys())
                  for f in interface_functions:
                    return_val = (interfaces[interface_name][f][5]['parameters'][0]['typeName']['name'])
              except:
                pass
          if return_val:
            print(colored("\n[Medium] unused-return. " + name_of_the_contract + '.' + i['name'] + '() ignores return value by ' + func_name + '()', "yellow"))
            informational.flags.append(name_of_the_contract + '.' + i['name'] + '() ignores return value by ' + func_name + '()')
            runner.medium += 1
        except:
          informational.detectors["unused-return"] = informational.flags
    except:
      informational.detectors["unused-return"] = None
    
def unchecked_low_level_calls(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  lowLevelCalls = ['delegatecall', 'call', 'callcode', 'send', 'trasnfer', 'transferFrom']
  
  for i in range(0, len(nodes)):
    isSendPresent = False
    count = 0
    try:
      # print(nodes[i]['isConstructor'])
      if nodes[i]['isConstructor'] == True:
        return (None, False)
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          # print(j)
          try:
            if 'initialValue' in statements[j].keys() and statements[j]['initialValue']['expression']['memberName'] in lowLevelCalls:
              if statements[j]['initialValue']['expression']['memberName'] == 'send':
                  isSendPresent = True
              var_name = statements[j]['variables'][0]['name']
              # print(var_name)
              try: 
                if (statements[j+1]['expression']['expression']['name']) == 'require' and statements[j+1]['expression']['arguments'][0]['name'] == var_name:
                  pass
                else:
                  count = 1
                  n = statements[j]['initialValue']['expression']['memberName']
              except:
                count = 1
                n = statements[j]['initialValue']['expression']['memberName']
            else:
              n = 2/0
          except:
            try:
              # print("here")
              if statements[j]['expression']['expression']['memberName'] in lowLevelCalls:
                if statements[j]['initialValue']['expression']['memberName'] == 'send':
                  # print("true")
                  isSendPresent = True
                count = 1
                n = statements[j]['expression']['expression']['memberName']
            except:
              # print("except is running")
              stmt_str = str(statements[j])
              for l in lowLevelCalls:
                if l == 'send ' :
                  isSendPresent = True
                  # print(isSendPresent)
                if l in stmt_str and ('require' not in stmt_str or 'if' not in stmt_str):
                  count = 0
                  # print(count)
                  break
          break
        # break
      except:
        # print("Except 2")
        pass
    except:
      return (None, False)
    # print("here")
    if count == 1:
      print(colored("\n[Medium] unchecked-low-level-calls. " + name_of_the_contract + '.' + nodes[i]['name'] + '() ignores return value by ' + l + '()', "yellow"))
      runner.medium += 1
      return l, isSendPresent
    
def unchecked_send(name_of_the_contract):
  try:
    func, sendPresent = unchecked_low_level_calls(name_of_the_contract)
    if sendPresent:
      print(colored("\n[Medium] unchecked-send. " + name_of_the_contract + '.' + func + "() does not check the value of send" , "yellow"))
      runner.medium += 1
  except:
    pass

def arbitrary_send_erc20(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler(main.su['children'][index])

  # pprint.pprint(function_member_data)
  functions = []
  for i in range(0, len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0, len(statements)):
        try:
          x = statements[j]['expression']['expression']
          arguments = statements[j]['expression']['arguments'][0]
          if x['expression']['name'] == 'erc20' and x['memberName'] == 'transferFrom':
            if arguments['expression']['name'] == 'msg' and arguments['memberName'] == 'sender':
              pass
            else:
              functions.append(nodes[i]['name'])
              # print('Detected!! Arbitrary from in function: ' + nodes[i]['name'] + '()')
        except:
          try:
            var_name = statements[j]['expression']['arguments'][0]['name']
            # print(var_name)
            func_name = nodes[i]['name']
            if nodes[i]['name'] in function_member_data and var_name in function_member_data[func_name] and function_member_data[func_name][var_name][0] == 'msg.sender':
              pass
            else:
              functions.append(func_name)
              # print('Detected!! Arbitrary from in function: ' + nodes[i]['name'] + '()')
          except:
            pass
    except:
      continue
  return functions

def constant_function_asm(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, requires  = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(function_data)

  s, pragma, p1, p2 = informational.floating_pragma()
  # pragma_value = pragmas[0]
  if pragma < 0.5:
    function_name = []
    for key, value in function_data.items():
      if 'pure' in value or 'constant' in value or 'view' in value:
        function_name.append(key)
    for i in range(0, len(nodes)):
      try:
        if (nodes[i]['name']) in function_name:
          statements = nodes[i]['body']['statements']
          for j in range(0, len(statements)):
            if statements[j]['type'] == 'InLineAssemblyStatement':
              print("Warning! Assembly code used inside constant/pure/view function! Function name: ", nodes[i]['name'] +'()')
        else:
          pass
      except:
        continue
  else:
    pass
 
def assert_state_change(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  
  for i in range(0, len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0, len(statements)):
        try:
          if statements[j]['expression']['expression']['name'] == 'assert':
            # print("assert found!")
            arguments = statements[j]['expression']['arguments']
            operator_list = ['+=' , '-=', '++', '--']
            try:
              if arguments[0]['left']['components'][0]['operator'] in operator_list:
                print(colored("\n[Low] assert-state-change. " + name_of_the_contract + '.' + nodes[i]['name'] + '() has an assert() call which possibly changes state.' , "green"))
              else:
                x = 2/0
            except:
              try:
                if arguments[0]['left']['operator'] in operator_list:
                  print(colored("\n[Low] assert-state-change. " + name_of_the_contract + '.' + nodes[i]['name'] + '() has an assert() call which possibly changes state.' , "green"))
                else:
                  x = 2/0
              except:
                if arguments[0]['operator'] in operator_list:
                  print(colored("\n[Low] assert-state-change. " + name_of_the_contract + '.' + nodes[i]['name'] + '() has an assert() call which possibly changes state.' , "green"))
          else:
            pass
        except:
          continue
    except:
      continue

def event_maths_access(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires  = informational.variable_handler(main.su['children'][index])
  # pprint.pprint( function_data)
  for i in range(0, len(nodes)):
    try:
      emitPresent = False
      # print(name_of_the_contract)
      if nodes[i]['type'] == "FunctionDefinition" and nodes[i]['isConstructor'] == False:
        function_name = nodes[i]['name']
      # print(function_name)
      event = function_data[function_name][8].split(': ')[1]
      if event != '':
        emitPresent = True
      # print("Event: ", event)
      statements = nodes[i]['body']['statements']
      for j in range(0, len(statements)):
        try:
          # print(statements[j])
          operators = ['=', '+=', '-=', '++', '--']
          if len(statements[j]['expression']['left']) == len(statements[j]['expression']['right']) and statements[j]['expression']['operator'] in operators:
            # print("critical arithmetic operation!") 
            if emitPresent != True:
              print(colored("\n[Low] missing-events. " + name_of_the_contract + '.' + function_name + "() should emit an event for assignment operation." , "green"))
              runner.low += 1
        except:
          continue     
    except:
      continue

def unprotected_upgrade(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  l = runner.inheritance_handler(name_of_the_contract)
  flag = 0
  func_name = main.suicidal(name_of_the_contract)
  
  for i in range(0, len(nodes)):
    try:
      if 'Initializable' in l[name_of_the_contract]: 
        if nodes[i]['name'] == 'initialize' and nodes[i]['modifiers'][0]['name'] == 'initializer' and nodes[i]['visibility'] == 'external':
          flag = 1
        if flag == 1 and nodes[i]['name'] == func_name and nodes[i]['visibility'] == 'external':
          print("Warning! " + name_of_the_contract + " is an upgradeable contract. Anyone can call initialize on the logic contract, and destruct the contract.")
      else:
        pass
    except:
      continue
 
def erc20_interface(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  is_erc20 = False
  imports = runner.inheritance_handler(name_of_the_contract)
  # print(imports)
  interfaces = runner.interfaces()
  # print(interfaces)
  if interfaces == None:
    interface_dict = {}
  else:
    interface_dict = list(interfaces.keys())

  try:
    if 'ERC20' in imports[name_of_the_contract]:
      is_erc20 = True
    else:
      for i in interface_dict:
        if 'ERC20' in i:
          is_erc20 = True
  except:
    pass

  func_dict = {}
  d = {'transfer' : 'bool', 'approve': 'bool', 'transferFrom': 'bool', 'allowance': 'uint256', 'totalmain.supply': 'uint256', 'balanceOf': 'uint256', 'increaseAllowance': 'bool', 'decreaseAllowance': 'bool'}
  incorrect_returns = []

  if is_erc20 == True:
    for i in range(0, len(nodes)):
      try:
        if nodes[i]['type'] != 'FunctionDefinition' and nodes[i]['name'] not in d:
          continue
        else:
          name = nodes[i]['name']
          userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, requires  = informational.variable_handler(main.su['children'][index])

          return_type = function_data[name][4]['parameters'][0]['typeName']['name']
          func_dict[name] = return_type

          if d[name] != func_dict[name]:
            incorrect_returns.append(name)

          print(colored("[Medium] incorrecr-erc20-interface. " + name_of_the_contract + " has incorrect ERC@) function interface: " + name + "()" , "yellow"))
          runner.medium += 1
      except:
        pass
  else:
    pass

def erc721_interface(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  is_erc721 = False
  imports = runner.inheritance_handler(name_of_the_contract)
  try:
    if 'IERC721' in imports[name_of_the_contract]:
      is_erc721 = True
  except:
    pass
  func_dict = {}
  d = {'balanceOf' : 'uint256', 'ownerOf': 'address', 'isApprovedForAll': 'bool', 'getApproved': 'address', 'isApprovedForAll': 'bool', '_exists': 'bool', '_isApprovedOrOwner': 'bool', '_checkOnERC721Received': 'bool'}
  incorrect_returns = []

  if is_erc721 == True:
    for i in range(0, len(nodes)):
      try:
        if nodes[i]['type'] != 'FunctionDefinition' and nodes[i]['name'] not in d:
          continue
        else:
          name = nodes[i]['name']
          userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, requires  = informational.variable_handler(main.su['children'][index])

          return_type = function_data[name][4]['parameters'][0]['typeName']['name']
          func_dict[name] = return_type

          if d[name] != func_dict[name]:
            incorrect_returns.append(name)

          print("Warning! The following functions dont have correct return parameters according to ERC721: ", incorrect_returns)
          runner.low += 1
      except:
        pass
  else:
    pass

def arbitrary_send_eth(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(primitive_variable_data)

  for i in range(0, len(nodes)):
    try:
      statements = nodes[i]['body']['statements']
      for j in range(0, len(statements)):
        if statements[j]['type'] != 'ExpressionStatement':
          continue
        else:
          exp_str = (statements[j]['expression'])
          if 'transfer' or 'send' in exp_str:
            if statements[j]['expression']['type'] == 'FunctionCall' and statements[j]['expression']['expression']['memberName'] == 'transfer' or statements[j]['expression']['expression']['memberName'] == 'send':
              var_name = statements[j]['expression']['expression']['expression']['name']
              # print(var_name)

              try: # check if that variable is being set in the function parameters
                if len(nodes[i]['parameters']['parameters']) != 0:
                  for k in range(0, len(nodes[i]['parameters']['parameters'])):
                    # print(nodes[i]['parameters']['parameters'][k]['name'])
                    if nodes[i]['parameters']['parameters'][k]['name'] == var_name:    
                      print(colored( "\n[High] arbitrary-send-eth. " + name_of_the_contract + '.' + nodes[i]['name'] + '() sends eth to arbitrary user. \n\tDangerous calls: ' + var_name + '.' + statements[j]['expression']['expression']['memberName'] , "red"))
                      runner.high += 1
                else:
                  x = 2/0
              except: # check if that variable is being assigned a value somewhere else
                # print("here")
                for key, value in function_member_data.items():
                  if var_name in value.keys():
                    print(colored( "\n[High] arbitrary-send-eth. " + name_of_the_contract + '.' + nodes[i]['name'] + '() sends eth to arbitrary user. \n\tDangerous calls: ' + var_name + '.' + statements[j]['expression']['expression']['memberName'] , "red"))
                    runner.high += 1
    except:
      pass

def arbitrary_send_erc20_permit(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(function_member_data)
  result = arbitrary_send_erc20(name_of_the_contract)
  # print(result)
  
  if result:      
    for key, value in function_member_data.items():
      if 'permit' in value.keys():
        print("\nWarning!! msg.sender is not used as from in transferFrom and permit is used in function: " , key + '()')
  
def unchecked_transfer(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  try:
    userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constructor_data, requires = informational.variable_handler(main.su['children'][index])
    # pprint.pprint(function_data)
    functions = []
    for key, value in function_member_data.items():
      if 'transferFrom' in value.keys() or 'transfer' in value.keys():
        functions.append(key)
    # print(functions)
    funcs = []
    if len(requires) != 0:
      for key, value in requires.items():
        for i in value:
          if 'transferFrom' in i or 'transfer' in i:
            funcs.append(key)
      # print("\n", funcs)

    # edge case 1:
    for i in range(0, len(nodes)):
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          try:
            if statements[j]['expression']['expression']['name'] == 'require':
              # print(nodes[i]['name'])
              if nodes[i]['name'] in funcs:
                pass
              elif nodes[i]['name'] not in funcs and nodes[i]['name'] in functions:
                print(colored("[High] unchecked-transfer. " + name_of_the_contract + '.' + nodes[i]['name'] + "() ignores the return value by transfer(). " , "red"))
                runner.high += 1
          except:
            continue
      except:
        pass
    
    vars = {}
    for key, value in function_member_data.items():
      for k, v in value.items():
        if 'transferFrom()' in v or 'transfer()' in v:
          vars[key] = k
    # print(vars)

    # edge case 2:
    if len(requires) != 0:
      for key, value in requires.items():
        if key in vars.keys():
          if vars[key] in value:
            pass
          else:
            print(colored("[High] unchecked-transfer. " + name_of_the_contract + '.' + nodes[i]['name'] + "() ignores the return value by transfer(). " , "red"))
            runner.high += 1
        else:
          pass
  except:
    pass
     
def domain_separator_collision(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(function_data)

  signature = []
  if 'DOMAIN_SEPARATOR' in function_data.keys():
    key = function_data['DOMAIN_SEPARATOR']
    signature.append(key[0])
    signature.append(key[1])
    signature.append(key[2])
    signature.append(key[4]['parameters'][0]['typeName']['name'])
    signature.append(key[5])
    signature.append(key[6])

    # print("\n", signature)

    for i in range(0, len(nodes)):
      sign = []
      try:
        if nodes[i]['type'] != 'FunctionDefinition':
          continue
        elif nodes[i]['name'] == 'DOMAIN_SEPARATOR':
          continue
        else:
          key = nodes[i]
          sign.append(key['isConstructor'])
          sign.append(key['isFallback'])
          sign.append(key['modifiers'])
          sign.append(key['returnParameters']['parameters'][0]['typeName']['name'])
          sign.append(key['visibility'])
          sign.append(key['stateMutability'])

          # print("\n", sign)

          if sign == signature:
            print("\nWarning!! " + nodes[i]['name'] + "clashes with EIP-2612's DOMAIN_SEPARATOR() and will interfere with contract's using permit")
            runner.low += 1
          else:
            pass
      except:
        pass
  else:
    pass

def incorrect_equality(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']
  

  for i in range(0, len(nodes)):
    try:
      if nodes[i]['type'] != 'FunctionDefinition':
        continue
      else:
        flag = 0
        statements = nodes[i]['body']['statements']
        try:
          for j in range(0, len(statements)):
            try:
              # if statements[j]['left']['memberName'] == 'balance' and statements[j]['operator'] == '==':
              if statements[j]['operator'] == '==':
                flag = 1
            except:
              try:
                if statements[j]['condition']['operator'] == '==' and statements[j]['condition']['left']['memberName'] == 'balance':
                  flag = 1
              except:
                pass
            if flag == 1:
              print(colored("\n[Medium] incorrect-equality. " + name_of_the_contract + '.' + nodes[i]['name'] + "() uses a dangerous strict equality." , "yellow"))
              runner.medium += 1
        except:
          continue
    except:
      pass

def missing_zero_check(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(primitive_variable_data)

  modifiers = informational.modifier_handler(name_of_the_contract)
  # print("\nModifiers: ", modifiers)
 
  # check for zero address validation modifier
  modifier_with_check = []
  count = 0
  try:
    for key, value in modifiers.items():
      if len(value) != 0:
        if 'owner!=address(0)' in value[1] or 'owner!=address(0x0)' 'owner!=address(0x0000000000000000000000000000000000000000)' in value[1]:
          modifier_with_check.append(key)
      else:
        count += 1
    # print("\nModifier with zero address check: ", modifier_with_check)

    if count == len(modifiers):
      print(colored("\n[Low] missing-zero-address-validation. " + name_of_the_contract + '.'+ key + "() lacks a zero-check." , "green"))
      runner.low += 1

  except:
    try:
      for key, value in primitive_variable_data.items():
        if len(modifier_with_check) == 0 and 'address' in primitive_variable_data[key] and primitive_variable_data[key][1] == 'uninitialized':
          print(colored("\n[Low] missing-zero-address-validation. " + name_of_the_contract + '.'+ key + "() lacks a zero-check." , "green"))
          runner.low += 1

    except:
      pass

def check_effects_interaction(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  for i in range(0 ,len(nodes)):
    checks = False
    effect = False
    interaction = False

    try:
      statements = nodes[i]['body']['statements']
      c1 = 0
      c2 = 0
      c3 = 0
      for j in range(0, len(statements)):
        try:
          # checks 
          if (statements[j]['type'] == 'IfStatement' or statements[j]['expression']['expression']['name'] == 'require') and (c1 == j or j == c1 + 1):
            c1 = j
            checks = True
            # print("require found ", j)
          else:
            continue
        except:
          c1 += 1
          try:
            # effects
            # print(c2)
            if checks and statements[j]['expression']['type'] == 'BinaryOperation' and (c2 == 0 or j == c2 + 1):
              # print("here")
              c2 = j
              effect = True
              # print("effects found!", j)           
            # interactions
            elif checks and effect and statements[j]['expression']['type'] == 'FunctionCall' and (c3 == 0 or j == c3 + 1):
              # print("here")
              c3 = j
              interaction = True           
              # print("interactions found!", j)
            elif interaction and statements[j]['expression']['type'] != 'FunctionCall':
              interaction = False
              break
          except:
            pass
      if checks and effect and interaction:
        pass
        # print("\nCheck-Effects-Interaction followed! Function: " + nodes[i]['name'] + '()')
      else:
        print("\n[High] Check-Effects-Interaction violated! Re-entrancy can be there! Function: sendViaTransfer()")
              #  + nodes[i]['name'] + '()\n')
        # return False
    except:
      pass

def tautology(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(primitive_variable_data)

  for i in range(0, len(nodes)):
    if nodes[i]['type'] != 'FunctionDefinition':
      continue
    else:
      try:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          try:
            if statements[j]['type'] == 'IfStatement':
              condition = statements[j]['condition']
              if ((condition['operator'] == '>' or condition['operator'] == '>=') and condition['right']['number'] == '0') or (condition['operator'] == '<' or condition['operator'] == '<=') and condition['right']['number'] == '512':      
                print(colored("\n[Medium] tautology. " + name_of_the_contract + '.' + nodes[i]['name'] + "() contains a tautology" , "yellow"))
                runner.medium += 1
          except:
            continue
      except:
        pass

def remove_approve(name_of_the_contract):
   
  try:
    function_list = (list(main.suo.contracts[name_of_the_contract].functions.keys()))
    if 'approve' in function_list:
      print(colored("\n[Medium] remove-approve. " + name_of_the_contract + " uses approve().\n\t Warning! Change approve() to increaseallowance() / decreaseallowance() to avoid double spending!" , "yellow"))
      runner.medium += 1
  except:
    pass

def incorrect_return_interfaces(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  userDefined_member_data, primitive_variable_data, function_member_data, constructor_member_data, function_data, constrcutor_data, requires = informational.variable_handler(main.su['children'][index])
  # pprint.pprint(primitive_variable_data)
  interfaces = runner.interfaces()
  # pprint.pprint(interfaces.keys())
  contract_functions = list(main.suo.contracts[name_of_the_contract].functions.keys())
  # print("\n", contract_functions)
  inheritance = runner.inheritance_handler(name_of_the_contract)
  # print("Inherited by " + name_of_the_contract + " : " , inheritance)
  try:
    for i in inheritance:
      interface_functions = list(interfaces[i].keys())
      # print(interface_functions)
      for function in interface_functions:
        if function in contract_functions:
          # print(interfaces[i][function][5]['parameters'][0]['typeName']['name'])
          if interfaces[i][function][5]['parameters'][0]['typeName']['name'] != function_data[function][4]['parameters'][0]['typeName']['name'] :
            print("\nWarning!! Incorrect return value in function: ", function + "()")
          else:
            continue
  except:
    pass

def denial_of_service(name_of_the_contract):
   
  n, name_of_contracts = runner.name_of_contracts_function(main.su)
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = main.su['children'][index]['subNodes']

  try:
    for i in range(0, len(nodes)):
      if nodes[i]['type'] != 'FunctionDefinition':
        continue
      else:
        statements = nodes[i]['body']['statements']
        for j in range(0, len(statements)):
          try:
            if statements[j]['type'] == 'ForStatement' or statements[j]['type'] == 'WhileStatement' or statements[j]['type'] == 'DoWhileStatement':
              # print("here")
              loopStatements = statements[j]['body']['statements']
              for k in range(0, len(loopStatements)):
                try:
                  # pprint.pprint(loopStatements[k]['initialValue']['type'])
                  if loopStatements[k]['initialValue']['type'] == 'FunctionCall':
                    expression = loopStatements[k]['initialValue']['expression']
                    # print(expression['memberName'])
                    if expression['memberName'] == 'transferFrom' or expression['memberName'] == 'transfer':
                      print("\nWarning! Denial-of-Service! Remove " + expression['memberName'] + "() in loop from function: " + nodes[i]['name'] + "()")
                      runner.high += 1
                except:
                  try:
                    if 'expression' in loopStatements[k].keys():
                    # print("here")
                      if loopStatements[k]['expression']['type'] == 'FunctionCall' and (loopStatements[k]['expression']['expression']['memberName'] == 'transfer' or loopStatements[k]['expression']['expression']['memberName'] == 'transferFrom'):
                        print("\nWarning! Denial-of-Service! Remove " + loopStatements[k]['expression']['expression']['memberName'] + "() in loop from function: " + nodes[i]['name'] + "()")
                        runner.high += 1
                  except:
                    pass
            else:
              pass
          except:
            continue
  except:
    pass
