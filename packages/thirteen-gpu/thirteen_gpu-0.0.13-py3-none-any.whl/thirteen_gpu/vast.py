import os
import json
import subprocess

def vast_on():
    
    instances = json.loads(subprocess.check_output("vast show instances --raw", shell=True))
    
    for instance in instances:
        if instance["actual_status"] == "exited":
            os.system(f"vast start instance {instance['id']}")
            
            print(f"Starting instance {instance['id']}")
    
    
def vast_off():
        
    instances = json.loads(subprocess.check_output("vast show instances --raw", shell=True))
    
    for instance in instances:
        if instance["actual_status"] == "running":
            os.system(f"vast stop instance {instance['id']}")
            
            print(f"Stopping instance {instance['id']}")