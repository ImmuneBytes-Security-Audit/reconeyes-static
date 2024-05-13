import shutil
from solidity_parser import parser
from termcolor import colored
import solcx
import os
from os import chdir as cd
from zipfile import ZipFile
import pprint

global name_of_contracts
global imports
imports = []

# PIPELINE
def pipeline(filename):
  # if FileHandler(filename) == filename:
    pragma_value = compiler(filename)
    if pragma_value and compilation == True:
      # print("ast generation start")
      if ast(filename):
        n, name_of_contracts = name_of_contracts_function(su)
        # print("pipeline success!")
        return su, suo, n, name_of_contracts, pragma_value
    else:
      print("pipeline failed!")
      return 0

# def FileHandler(filename):
  # filename = "SimpleStorage.sol"
  # # print("in runner.FileHandler: ", filename)
  # return filename

def flattener(filename):
  ext = filename.split('.')
  try:
    # FOR SINGLE CONTRACT WHICH CONTAINS OPENZEPLLIN IMPORTS
    if "sol" in filename:
      print("sol file uploaded")
      source_file = '/home/tool/ImmuneLite0.1v/uploaded_contracts/'+ filename
      destination_folder = '/home/tool/ImmuneLite0.1v/Foundry/src/'
      shutil.copy(source_file, destination_folder)
      # print(os.getcwd())
      cd('../Foundry/')
      os.system('forge flatten src/* >> /home/tool/ImmuneLite0.1v/flat_contracts/filename.sol')
      os.system('grep -v SPDX /home/tool/ImmuneLite0.1v/flat_contracts/filename.sol > ../flat_contracts/temp.sol')
      cd('../Runner/')
      print("single file flatten working")
      return 1
    
    # FOR ZIP UPLOADS WHICH NEED TO BE FLATTENED
    elif "zip" in filename:
      source_file = '/home/tool/ImmuneLite0.1v/zip_contracts/'+ filename
      print("zip file uploaded: ", filename)
      with ZipFile('/home/tool/ImmuneLite0.1v/zip_contracts/'+ filename, 'r') as f: # unzip the zip file
        f.extractall()
      path = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/config.txt' #we are inside the Runner directory so the uploaded zip file will be unzipped into Runner 
      fileExists = os.path.exists(path) #check if config.txt is present or not
      # print(fileExists)
      # read config.txt
      if fileExists:
        cd (ext[0])
        with open('config.txt', 'r') as f:
          for line in f:
            if line.startswith('main_contract'):
              main_contract = line.split('==')[1]
            if line.startswith('contract_name'):
              contract_name = line.split('==')[1]
            if line.startswith('framework'):
              framework = line.split('==')[1]
      else:
        print("No config.txt")
      # print(contract_name, main_contract, framework)
 
      # IF THE UPLOADED ZIP FILE IS A FRAMEWORK PROJECT
      if 'Hardhat' in framework or framework == 'Truffle' or framework == 'Brownie':
        source = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/'
        destination_folder = '/home/tool/ImmuneLite0.1v/Foundry/src'
        cd(source)
        dirs = list(os.listdir(source))
        for d in dirs:
          # print(d)
          if d == 'contracts':
            path = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/' + 'contracts/'
            contracts = list(os.listdir(path))
            # print(contracts)
            for c in contracts:
              # print(c)
              source = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/' + 'contracts/' + c
              desti = '/home/tool/ImmuneLite0.1v/Foundry/src/'
              shutil.copy(source , destination_folder) 
        print("contracts copied into Foundry src")
  
      elif framework == 'Dapptools' or framework == 'Foundry':
        # print(framework)
        source = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/'
        destination_folder = '/home/tool/ImmuneLite0.1v/Foundry/src'
        cd(source)
        dirs = list(os.listdir(source))
        for d in dirs:
          # print(d)
          if d == 'src':
            path = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/' + 'src/'
            contracts = list(os.listdir(path))
            # print(contracts)
            for c in contracts:
              # print(c)
              source = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/' + 'src/' + c
              desti = '/home/tool/ImmuneLite0.1v/Foundry/src/'
              shutil.copy(source , destination_folder) 
        print("contracts copied into Foundry src")
  
      elif framework == 'NA' or framework == '' or framework == None:
        print("No framework specified")
        print("this", os.getcwd())
        with os.scandir() as entries:
          for entry in entries:
            # print(entry)
            source = '/home/tool/ImmuneLite0.1v/Runner/' + ext[0] + '/' + entry.name
            desti = '/home/tool/ImmuneLite0.1v/Foundry/src'
            shutil.copy(source , desti) 
        print("files copied")
        cd('/home/tool/ImmuneLite0.1v/Foundry/src')
        os.system('rm config.txt')
  
      else:
        print("None of the frameworks is working!")  
      
      # os.system('ls -l')
      cd('/home/tool/ImmuneLite0.1v/Foundry/src')
      cd('../')
      print("flattener start")
      os.system('forge flatten src/* >> /home/tool/ImmuneLite0.1v/flat_contracts/filename.sol')
      print("files flattened")
      os.system('grep -v SPDX /home/tool/ImmuneLite0.1v/flat_contracts/filename.sol > /home/tool/ImmuneLite0.1v/flat_contracts/temp.sol')
      # print(os.getcwd())
      cd('/home/tool/ImmuneLite0.1v/flat_contracts/')
      print("zip upload flatten working !!")
      return 1
  
    # IF NONE OF THE IF-ELSE WORKS, THEN IT'S NEITHER .SOL NOT .ZIP
    else:
      return 0
  except:
    print("Flattening Failed!")
    return 0

def compiler(filename):
  global compilation
  try:
    # extract solidity version from the contract file
    path = "SimpleStorage.sol"
    # path = "C:/Users/DELL/Documents/GitHub/mercury/api code/uploads/" + filename
    with open(path , 'r') as f:
    # with open('/home/tool/ImmuneLite0.1v/flat_contracts/temp.sol', 'r') as f:
      for line in f:
        if line.startswith('pragma'):
          pragma_value = (line.split(' ')[-1].replace(';', ''))
          pragma_value = pragma_value.replace('\n', '')
          # print(pragma_value)
      if '^' in pragma_value:
        pragma_value = pragma_value.split('^')[1]
        print(colored("\nFloating Pragma Detected!", "red"))
        # print(pragma_value)
      if '>=' in pragma_value:
        pragma_value = pragma_value.split('>=')[1]
    # print(pragma_value)
    lst = solcx.get_installed_solc_versions()
    # print(lst)
    flag = 0
    for i in range(0, len(lst)):
      if pragma_value == str(lst[i]):
        flag = 1
      else:
        flag = 0

    # print(pragma_value)

    # Set the solcx version
    if flag == 0 and i == len(lst) - 1:
      print("\nInstalling solc version ...")
      solcx.install_solc(pragma_value, show_progress=False)
      solcx.set_solc_version(pragma_value)
      print("Installated version: ", pragma_value)
  
    # compile the solidity code through solc, if compilation is successful -- then only run the detectors otherwise display the compilation error
    # solcx.compile_files(["/home/tool/ImmuneLite0.1v/flat_contracts/temp.sol"],
    #                     output_values=["abi", "bin-runtime"],
    #                     solc_version=pragma_value)

    solcx.compile_files(["SimpleStorage.sol"],
                        output_values=["abi", "bin-runtime"],
                        solc_version=pragma_value)
    print(colored("\nCompilation successful!", "green"))
    compilation = True
  except Exception as e:
    print(colored("\nxxxxxxxxxxxx Compilation failed! xxxxxxxxxxxx\n", "red"))
    print(e)
    compilation = False
  return pragma_value

def ast(filename):
  global su
  global suo
  try:
    try:
      # name = "C:/Users/DELL/Documents/GitHub/mercury/api code/uploads/" + filename
      # name = "SimpleStorage.sol"
      sourceUnit = parser.parse_file(filename, loc=False)
      su = dict(sourceUnit)
      suo = parser.objectify(sourceUnit)
      # pprint.pprint(type(su))
      return 1
    except:
      ###### CODE TO HANDLE AST GENERATION FAILURE ######
      # print("AST Generation failed !!")
      with open(filename, 'r') as file:
        lines = file.readlines()
      # for (bool success, ) line
      with open(filename, 'w') as temp:          
        for line in lines:
          if "(bool success, " in line or "slot :=" in line:
            temp.write("//" + line)
          else:
            temp.write(line)
        temp.close()
      print("ast generation block end")
      # test = "/home/tool/ImmuneLite0.1v/Runner/test.sol"

      # GENERATE AST AFTER RESOLVING THE ISSUE
      sourceUnit = parser.parse_file(filename, loc=False)
      su = dict(sourceUnit)
      print("ast parsed")
      # os.system('rm /home/tool/ImmuneLite0.1v/Runner/test.sol')
      # print("test.sol file deleted")
      return 1
  except:
      print("AST Generation failed!")
      return 0

def contractHandler(su):
  # print(type(su))
  number_of_contracts = 0
  libraries = []
  others = 0  # for other nodes than contract
  try:
    for i in range(1, len(su['children'])):
      try:
        # print(type(su))
        if su['children'][i]['kind'] == 'contract' or su['children'][i]['kind'] == 'abstract' or su['children'][i]['kind'] == 'library':
          number_of_contracts += 1
          if su['children'][i]['kind'] == 'library':
            libraries.append(su['children'][i]['name'])
        else:
          others += 1
      except:
        others += 1
      try:
        if su['children'][i]['type'] == 'ImportDirective':
          imports.append((su['children'][i]['path']).split("\\")[-1])
      except:
        pass
    # print(number_of_contracts)
    return number_of_contracts
  except Exception as e:
      print("Error in contractHandler(): ", e)
      return 0

def name_of_contracts_function(su):
  # print("here")
  # print(len(su['children']))
  noc = contractHandler(su)
  n = ((len(su['children'])) - noc)
  if n != 0:
    name_of_contracts = []
    for i in range(1, len(su['children'])):
      try:
        if su['children'][i]['kind'] == 'contract' or su['children'][i]['kind'] == 'abstract' or su['children'][i]['kind'] == 'library':
          name_of_contracts.append(su['children'][i]['name'])
      except:
        pass
  # print(name_of_contracts)
  # print(n)
  return n, name_of_contracts

def interfaces():
  try:
    interfaces = {}
    for i in range(1, len(su['children'])):
      kind = su['children'][i]['kind']
      if kind == "interface":
        name = su['children'][i]['name']
      children = su['children']
      for i in children:
        if i['name'] == name:
          nodes = i['subNodes']
          function_name = []
          function_data = {}
          if len(i['subNodes']) == 0:
            interfaces[name] = []
          else:
            for k in range(0, len(i['subNodes'])):
              visibility = nodes[k]['visibility']
              isFallback = nodes[k]['isFallback']
              isReceive = nodes[k]['isReceive']
              modifiers = nodes[k]['modifiers']
              parameters = nodes[k]['parameters']
              returnParameters = nodes[k]['returnParameters']
              stateMutability = nodes[k]['stateMutability']
              function_name = i['subNodes'][k]['name']
              # print(function_name)
              function_data[function_name] = [
                visibility, isFallback, isReceive, modifiers, parameters,
                returnParameters, stateMutability
              ]
              interfaces[name] = function_data
      else:
        pass
    return interfaces
  except:
    pass

def inheritance_handler(name_of_the_contract):
  try:
    current_contract = {}
    for index in range(1, len(su['children'])):
      contracts_inherited = []
      try:
        if len(su['children'][index]['baseContracts']) > 0:
          for n in range(0, len(su['children'][index]['baseContracts'])):
            contracts_inherited.append(su['children'][index]['baseContracts'][n]['baseName']['namePath'])
            current_contract[su['children'][index]['name']] = contracts_inherited
          pass
        else:
          current_contract[su['children'][index]['name']] = []
      except:
        pass
    return current_contract[name_of_the_contract]
  except:
    pass

def require_handler(name_of_the_contract):
  n, name_of_contracts = name_of_contracts_function()
  index = name_of_contracts.index(name_of_the_contract) + n
  nodes = su['children'][index]['subNodes']
  # print("here")
  functions = {}
  try:
    for i in range(0, len(nodes)):
      requires = []
      if nodes[i]['type'] != 'FunctionDefinition' and nodes[i]['type'] != 'ModifierDefinition':
        continue
      else:
        try:
          name = nodes[i]['name']
          statements = nodes[i]['body']['statements']
          for j in range(0, len(statements)):
            try:
              if statements[j]['expression']['expression']['name'] == 'require':
                # print("here")
                requires.append('require')
                arguments = statements[j]['expression']['arguments']
                for argument in arguments:
                  if 'expression' in argument.keys():
                    try:
                      # print("here")
                      if argument['type'] == 'FunctionCall':
                        # print("here")
                        condition = argument['expression']['memberName']
                        requires.append("condition: " + condition)
                      else:
                        x = 2 / 0
                    except:
                      # print("running")
                      pass
                  elif argument['type'] == 'Identifier':
                    var = argument['name']
                    requires.append("variable: " + var)
                  elif argument['type'] == 'BinaryOperation':
                    # print("here")
                    try:
                      condition = argument['left']['number'] + argument['operator'] + argument['right']['number']
                      requires.append("functionCall: " + condition)
                    except:
                      try:
                        if argument['left']['type'] == 'MemberAccess' or argument['right']['type'] == 'MemberAccess':
                          condition = argument['left']['expression']['name'] + '.' + argument['left']['memberName'] + argument['operator'] + argument['right']['expression']['name'] + '.' + argument['right']['memberName']
                          requires.append(condition)
                        elif argument['right'][
                            'type'] == 'FunctionCall' and argument['left']['type'] == 'Identifier':
                          # print("here")
                          condition = argument['left']['name'] + argument['operator'] + argument['right']['expression']['name'] + '(' + argument['right']['arguments'][0]['number'] + ')'
                          # print(condition)
                          requires.append(condition)
                      except:
                        pass
            except:
              continue
        except:
          continue
        functions[name] = requires
    return functions
  except:
    print("Empty Contract")

high = 0
medium = 0
low = 0
info = 0
optimize = 0

def human_summary():
  print("High: ", high)
  print("Medium: ", medium)
  print("Low: ", low)
  print("Informational: ", info)
  print("Optimization: ", optimize)

# # delete scanned files
# os.system('rm /home/tool/ImmuneLite0.1v/flat_contracts/*')
# os.system('rm /home/tool/ImmuneLite0.1v/Foundry/src/*')
