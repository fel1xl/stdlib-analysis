# stdlib-analysis
stdlib-analysis is a program to analyse the packages within pythons standard library. stdlib-analysis has several functions 

1. Function 1 obtains all of the python packages in the standard library dependant on the python version installed. 'task1()' returns the python version, then the OS, followed by the number of importable packages and finally the first and last 5 importable standard library packages. Included within this function is further functions one of which obtains the entire list

2.  The 2nd function in stdlib-analysis obtains the names of all of the packages in the standard library which are not importable (depending on the python version detected). This is done by finding attempting to import each packages (finding whats in its namespace). 'task2()' returns the list of packages from the standard library which cannot be imported for the installed python version

3. The 3rd function calculates linking / dependency between standard library packages. This is acheieved through exploring the contents of the packages namespace using the vars function to return a dictionary. From this analysis of packages dependency, core packages are determined. 'task3()' returns the 5 most dependent packages form the standard library followed by the core packages.

4. The 4th and final function explores the contents of the packages using the OSwalk function. This function searches contents of packages determining those with the most and least lines of code as well as most and least classes. 'task4()' returns the 5 packages with most lines, 5 packages with least lines, 5 packages with most classes and a list of packages with no classes.  
