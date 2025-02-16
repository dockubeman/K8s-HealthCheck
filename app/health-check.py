import subprocess

def run_kubectl_command(command):
    try:
        result = subprocess.run(['kubectl'] + command.split(), capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error running command: {command}\n{result.stderr}")
            return None
    except Exception as e:
        print(f"Exception running command: {command}\n{str(e)}")
        return None

def check_nodes():
    print("Checking node status...")
    output = run_kubectl_command("get nodes")
    if output:
        print(output)

def check_pods():
    print("Checking pod status...")
    output = run_kubectl_command("get pods --all-namespaces")
    if output:
        print(output)

def check_deployments():
    print("Checking deployment status...")
    output = run_kubectl_command("get deployments --all-namespaces")
    if output:
        print(output)

def check_services():
    print("Checking service status...")
    output = run_kubectl_command("get services --all-namespaces")
    if output:
        print(output)

def check_pvc():
    print("Checking persistent volume claim status...")
    output = run_kubectl_command("get pvc --all-namespaces")
    if output:
        print(output)

def run_health_checks():
    check_nodes()
    check_pods()
    check_deployments()
    check_services()
    check_pvc()

if __name__ == "__main__":
    run_health_checks()