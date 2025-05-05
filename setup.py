# File to setup the project, run the command "python3 setup.py"
# Do not modify this file

# Check if venv was created, the venv should be named "flask"

import os, subprocess, sys

flaskVenvPath = 'flask'
instancePath = 'instance'

if not os.path.isdir(flaskVenvPath):
    print('Virtual env. not found, creating one')
    try:
        # subprocess.Popen('python3 -m venv flask', shell=True)
        proc = subprocess.Popen(f'python3 -m venv {flaskVenvPath}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        outs, errs = proc.communicate()
                
        if errs:
            raise Exception(errs.decode("utf-8"))
        
        print("Virtual env. created successfully")
        
    except Exception as e:
        print(str(e))
    
    finally:
        proc.kill()

else:
    print("Virtual environment exist, skipping creation")
    
if not os.path.isdir(instancePath):
    print('Instance folder not found, creating one and subfiles')
    
    filesUnderInstancePath = ['.env', 'config.py']
    for file in filesUnderInstancePath:
        try:
            pc = subprocess.Popen(f"touch {os.path.join(instancePath, file)}", stdout=subprocess.PIPE, shell=True)
            errs = pc.communicate()
            
            if errs:
                raise Exception(errs.decode("utf-8"))
        
        except Exception as e:
            print(str(e))
            sys.exit(0)
        
        finally:
            pc.kill()

else:
    print('''Instance folder does exist, create the following files under it if not exist\n
          - .env
          - config.py
          ''')
       
    