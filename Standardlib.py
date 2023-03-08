
'Task 1'

import importlib
import platform

"""This function, 'std_lib_list' returns list of importable packages in the standard library """
def std_lib_list():
    
    platform_num = ''.join(platform.python_version_tuple())    # Use platform module to get version tuple
    platform_num_minor = platform_num[1]                       # Slice version tuple to find minor version
    if int(platform_num_minor) >= 10:                          
        importlib.import_module('isort.stdlibs.py3'+platform_num_minor) # if else statement determining which 'isort'
    else:                                                               # function to use based on minor version
        import_version = importlib.import_module('isort.stdlibs.py3'+platform_num_minor)  
        imp_version_w_stdlib = import_version.stdlib
    list_of_importable = imp_version_w_stdlib
    if 'antigravity' in list_of_importable:
        list_of_importable.remove('antigravity')     #filtering out 'antigravity' and 'this'
    if 'this' in list_of_importable:
        list_of_importable.remove('this')
        
    list_b = []          # list of packages that do not contain _ (to get only modules)
                
    for word in list_of_importable:
        if '_' not in word:
            list_b.append(word)
        
    return list_b 

""" The function 'task1()' returns the first and last 5 importable modules, taken from 
    'std_lib_list()' and adds basic information like the python version  """

def task1():

    no_modules = len(std_lib_list())
    return print('python '+'.'.join(platform.python_version_tuple())+ ' on ' 
                 + platform.system()+'. ' 'StdLib contains '
                 + str(no_modules) + ' external modules and packages: ' +  ', '.join(std_lib_list()[0:5]) 
                 + '. . .' + ', '.join(std_lib_list()[-5:-1])+'.' )    #slicing for first and last 5 moduels
  
    

    

## --------------------------------

'Task 2'


""" The function 'get_real()' returns the list of all package names that can actually be imported
    This is done using try except, and handling the error to remove modules from the list that can't
    be imported"""
    
def get_real(package_names):
    list1 = package_names
    for word in package_names:
        try:                 #try to import module, use except to handle error when modeule can't be imported
            importlib.import_module(word)
        except:
            list1.remove(word)
    return list1


""" The function 'task2()' appends to a list the packages which are not allowed"""
def task2():
    allpackages = std_lib_list()
    allowed = get_real(std_lib_list())

    not_allowed = []    
    
    for a in allpackages:
        if a not in allowed:
            not_allowed.append(a)      #append packages that can't be imported to the note allowed lsit
        
    print("These StdLib packages on python " + '.'.join(platform.python_version_tuple()) 
          +' ' +platform.system()+ " are not importable:")
    print(', '.join(not_allowed))     # return function with other basic information
    
 
 
## ----------------------------------
## ----------------------------------
'Task 3'

#- - - -
""" Function 'module_dependency()' takes module names list and a single module name as a string
    and conducts a vars on the name to get the modules dictionary. From this dictionary, a for loop 
    is used to search and dtermine if any of the names in the dictionary can be matched to module names in the
    list provided, therefore indicating dependency."""

def module_dependency(module_names, name):
    a1= importlib.import_module(name)  # First, provided name is taken and imported, then stored in variable
    x1 = (vars(a1).keys())             # Vars function is then used on this variable (a1) to find dict of 
                                       # that module name 
    dependent_modules = []
    
    for value1 in module_names:
        if value1 in x1 and value1 != name:
            dependent_modules.append(value1)
              
    return dependent_modules            # dependent modules are returned

#- - - -
""" 'Top5_dependent' - this function uses a dictionary and for loop to find the top 5 most dependent
     modules. The dictionary takes the key as name of the module and the length of the previous function 
     'module_dependency' for the variables i and x2. """
def top5_dependent():
    dict1={}
    x2 = get_real(std_lib_list())
    for i in x2:
        
        dict1[i]=len(module_dependency(x2, i)) #module_dependency function applied to all i and importable 
                                                # modules from std lib which is given by x2  
        sorteddict1 = sorted(dict1.items(), key=lambda x:x[1], reverse = True)
        #dictionary sorting use lambda function used, and the 2nd element is sliced. Reverse is used
        #to get the list in descending order. Finally the function is returned in string form, sliced
        #as required ([0:5])
 
    return ("The 5 most dependent stdlib packages are:" + str(sorteddict1[0:5]))

#- - - -     

""" The function 'core_modules' uses a for loop and cycles all importable modules through the original 
    'module_dependency' function, as in previous function. A condition is set to check if the module
    dependency returned by 'module_deoendency' function is empty, given by == []"""
def core_modules():

    core_list = []
    importable_packages = get_real(std_lib_list())    #x3 is the importable modules to be cycled through dependency function
    for i in importable_packages:
       dependency_output = (module_dependency(importable_packages, i))   #cycling through modules as in previous
       #print(zz)
       if dependency_output == []:   # if no dependency / = to empty list then append to core list
            core_list.append(i)
    return core_list

#- - - -
""" This function 'task3()' returns the top 5 dependent and the core modules using the task 3 functions
    defined above """
def task3():
       
    print(top5_dependent()) 
    
    print ('The '+str(len(core_modules())) +' core packages are: ' + str(core_modules()))
    

## ----------------------------------
## ----------------------------------

'Task 4'
 

""" Function 'explore_package' is the base function used in task 4. This function conducts vars
    on the module to checks whether the given module is either just a file, or has a path to multiple 
    files. 
    
    In the case where the module is just a file the file is simply opened using __file__
    and the lines read and classes counted and sum returned.
    
    In the case the module is a path, os walk is used to go through the directory to each file.
    lines and classes are then counted and sum returned
    
    In both cases, the .py suffix is checked to ensure only python files are being opened and analysed
     """

def explore_package(a_package):      ## takes a package in string form
    import os   
    import_package = importlib.import_module((a_package))
    resources = (vars(import_package))          # The dictionary returned for the given package after the 
                                                # package has been imported in line 182
    sumint = 0
    classes = 0
    
    
    if "__path__" in resources.keys():    # searching dictionary keys provided by vars to try and find
                                          # the term '__path__' indicating the module has a path
        
        for (root,dirs,files) in os.walk(resources['__path__'][0]): # OS.walk function then used to walk   
                                                                    #thorugh directory if __path__ found
            path = root      # the root provided is the path, which is then used in os.path later
            
            for filename in files:                      
                if filename.endswith(".py"):        #condition to check .py files only
                    
                    with open (os.path.join(path,filename)) as file:    #using with open and os.path to 
                                                                        #open file and then dispose of it
                        
                
                        r2 = file.readlines()               # reading file, but as lines in a list
                        
                                                 # finding total number of lines, (counting length of
                        sumint += len(r2)        # list of lines given by r2 above)
                        for line in r2 :       
                            line = line.strip()          #stripping file so all txt moved to col.1 for next step
                            if line.startswith('class'): #finding classes and adding to total 'classes'
                                classes += 1          
                            
                       
            return (sumint, classes)   #return linecount and classes tuple
        
    
  
   
    
    elif "__file__" in resources.keys():      #avove process repeated for file, except without oswalk
        
        
        filename = resources['__file__']  
        if filename.endswith(".py"):
                with open(filename) as file:
                    lines = file.readlines()
                    sumlines = (len(lines))
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('class'):
                            classes += 1
                return (sumlines, classes) 
      
            
             
    else:             #else statement to return (0, 0) when a module is neither a file or path (not count)
        return(0, 0)

 # - - - -   

""" 'tuple_list()' is used to loop all importable packages through the above explore package function
     During this process, nonetypes are filtered out to prevent issues when indexing later
     A string (the module name) and a list of tuples (line count and class) is returned"""

def tuple_list():
    importable_packages = get_real(std_lib_list())
    tuples = []
   
    #dictx = {}
    
    #loc_dict = {}
    #class_dict = {}
    
    for i in importable_packages:        # looping packages through explore package function
        z = explore_package(i)
        if z is not None:                #filtering out nonetypes
            #print(type((i, z)))
            tuples.append((i, z))
    return tuples

#- - - - 

""" 'loc_dict_top5()' returns the modules with the top 5 highest line count. This is done by creating a
     tuple with i (module name) as the key, and the line count as the value. This is done by slicing the
     list created in 'tuple_list()' above."""

def loc_dict_top5():
    pairs = {}    
    for i in tuple_list(): 
        module_name = i[0]          #slicing to get module name which is first element in tuple list
        line_count = i[1][0]       #slicing 1st element OF the 2nd element in tuple list. (slicing tuple) for line count
       
        pairs[module_name] = line_count     #These values are then put into dictionary
    
    sorted_pairs = {k:v for k,v in sorted(pairs.items(), key= lambda item: item[1], reverse=True)} 
                    # The 'sorted' function is then used to sort dictionary in descending order
                    #This allows the dictionary to be sorted by the 2nd item [1] which is the line count


    final_sorted = list(sorted_pairs.keys())[0:5]    #slicing as required to reurn final list
    print('The 5 packages with most lines are:')
    for i in final_sorted:     
        print(i,sorted_pairs[i])
        
 
#- - - -   
""" Function 'loc_dict_bottom5' does the same as the above function except for bottom 5"""      
def loc_dict_bottom5():
    pairs = {}    
    for i in tuple_list(): 
        module_name = i[0]
        line_count = i[1][0]
       
        pairs[module_name] = line_count 
    sorted_pairs = {k:v for k,v in sorted(pairs.items(), key= lambda item: item[1], reverse=True)}      

        
    final_reverse_sorted = list(sorted_pairs.keys())[-6:-1] #sliced as required
    print('The 5 packages with the least lines are: ')
    for i in final_reverse_sorted:
        print(i, sorted_pairs[i])        
 
        
#- - - -  
""" 'class_dict_top5' finds the 5 modules with the most amount of classes. It uses the same
     mechanics as the 2 above functions for finding line count, with minor differences"""
def class_dict_top5():
    pairs = {}    
    for i in tuple_list(): 
        module_name = i[0]
        class_count = i[1][1]  #instead of slicing fof the first element of the tuple, this 
                               #time the second element is sliced which is class count
        pairs[module_name] = class_count 
    sorted_pairs = {k:v for k,v in sorted(pairs.items(), key= lambda item: item[1], reverse=True)}     

    final_sorted = list(sorted_pairs.keys())[0:5]
    print('The 5 packages with most classes are:')    
    for i in final_sorted:
         
        print(i,sorted_pairs[i])

#- - - -      
      
""" Function 'no_classes' like the above function which finds top 5 classes, slices tuple for class count
    However this function then has a condition for the class count to be 0 for the relevent module name, i
    to be appended to the no class list"""
 
def no_classes():
    list_noclass = []
    for i in tuple_list(): 
        module_name = i[0]
        class_count = i[1][1]
        
        if class_count == 0:         #condition, if there are 0 classes counted append module name to list
            list_noclass.append(module_name)
    print('The modules with no classes are: ' + str(list_noclass))


#- - - - 

""" 'Task 4' uses all of the above functions to return 5 largest modules in terms of line count, 5 
     smallest modules in terms of line count, top 5 modules in terms of class count and modules 
     which do not containany classes"""
def task4():
    (loc_dict_top5()) 
    print()
    (loc_dict_bottom5()) 
    print()
    (class_dict_top5())
    print()
    (no_classes())



  
    



  

    


