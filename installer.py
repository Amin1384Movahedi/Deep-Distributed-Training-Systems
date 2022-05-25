import os 
import sys

modules = ['tensorflow', 'pandas', 'numpy', 'scikit-learn', 'matplotlib', 'zipfile']
not_installed = []

for module in modules:
    try:
        exec(f'import {module}')
    except:
        not_installed.append(module)

if len(not_installed) == 0:
    sys.exit('All of needed modules are installed already!')

print('\n'*30)
print(f'These modules are not installed {not_installed}')
status = input('Do you wanna install them automatically? (Y/n) ')[0].lower()

if status == 'y':
    for module in not_installed:
        sys.system(f'pip install {module}') 

elif status == 'n':
    sys.exit('GoodBy.') 

else:
    sys.exit('Abort!')

print('\n'*30)
print('All of needed modules are installed successfully!')