import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def run_kubectl_command(command):
    try:
        result = subprocess.run(['kubectl'] + command.split(), capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            raise subprocess.CalledProcessError(result.returncode, command, result.stderr)
    except subprocess.CalledProcessError as e:
        return f"Error running command '{e.cmd}':\n{e.output}"
    except Exception as e:
        return f"Exception running command: {command}\n{str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_nodes')
def check_nodes():
    output = run_kubectl_command("get nodes")
    flash_message(output)
    return render_template('output.html', title='Node Status', output=output)

@app.route('/check_pods')
def check_pods():
    output = run_kubectl_command("get pods --all-namespaces")
    flash_message(output)
    return render_template('output.html', title='Pod Status', output=output)

@app.route('/check_deployments')
def check_deployments():
    output = run_kubectl_command("get deployments --all-namespaces")
    flash_message(output)
    return render_template('output.html', title='Deployment Status', output=output)

@app.route('/check_services')
def check_services():
    output = run_kubectl_command("get services --all-namespaces")
    flash_message(output)
    return render_template('output.html', title='Service Status', output=output)

@app.route('/check_pvc')
def check_pvc():
    output = run_kubectl_command("get pvc --all-namespaces")
    flash_message(output)
    return render_template('output.html', title='PVC Status', output=output)

def flash_message(output):
    if "Error" in output or "Exception" in output:
        flash(output, 'error')
    else:
        flash("Command executed successfully", 'success')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)