import os 
import sys

# List of required modules
modules = ['tensorflow', 'pandas', 'numpy', 'scikit-learn', 'matplotlib', 'zipfile']
not_installed = []

# Check the required modules, if any of them are not installed, they will be added to the not_installed list.
for module in modules:
    try:
        exec(f'import {module}')
    except:
        not_installed.append(module)

# If length of not_installed list was 0, that means all of required modules are installed already.
if len(not_installed) == 0:
    sys.exit('All of needed modules are installed already!')

# Getting the installation permission from user.
print('\n'*30)
print(f'These modules are not installed {not_installed}')
status = input('Do you wanna install them automatically? (Y/n) ')[0].lower()

# Start installing the modules.
if status == 'y':
    for module in not_installed:
        os.system(f'pip install {module}') 

elif status == 'n':
    sys.exit('GoodBy.') 

else:
    sys.exit('Abort!')

print('\n'*30)
print('All of needed modules are installed successfully!')