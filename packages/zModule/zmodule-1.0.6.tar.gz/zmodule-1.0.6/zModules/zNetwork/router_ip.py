import subprocess

def get_router_ip() -> str:

    result = subprocess.run(["ipconfig"], capture_output = True, text = True, check=True)

    lines = result.stdout.split('\n')

    for line in lines:

        if "Standardgateway" in line or "Default Gateway" in line:  #! german / english
        
            ip = line.split(":")[-1].strip()
            
            return ip