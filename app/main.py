from flask import Flask, request, jsonify, render_template_string
import subprocess
import yaml
import os
import hashlib

app = Flask(__name__)

# Intentional weakness 1: hardcoded debug mode
# Bandit will flag this as B201 (flask debug mode)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'DevSecOps demo application'
    })

@app.route('/ping')
def ping():
    """
    Intentional weakness 2: OS command injection via shell=True
    Bandit will flag this as B602 (subprocess with shell=True)
    """
    host = request.args.get('host', 'localhost')
    result = subprocess.run(
        f'ping -c 1 {host}',
        shell=True,          # <-- B602: shell injection risk
        capture_output=True,
        text=True,
        timeout=5
    )
    return jsonify({'output': result.stdout})

@app.route('/config')
def load_config():
    """
    Intentional weakness 3: unsafe YAML load
    Bandit will flag this as B506 (yaml.load without Loader)
    """
    config_data = request.args.get('data', '{}')
    config = yaml.load(config_data)   # <-- B506: should use yaml.safe_load
    return jsonify({'config': str(config)})

@app.route('/hash')
def weak_hash():
    """
    Intentional weakness 4: use of weak hash algorithm
    Bandit will flag this as B303 (use of MD5)
    """
    data = request.args.get('data', 'test')
    result = hashlib.md5(data.encode()).hexdigest()   # <-- B303: MD5 is weak
    return jsonify({'hash': result})

@app.route('/render')
def template_render():
    """
    Intentional weakness 5: Server-Side Template Injection (SSTI)
    Bandit will flag this as B703 / B702
    """
    user_input = request.args.get('name', 'World')
    # NEVER do this in real code - renders user input directly as a template
    template = f"<h1>Hello {user_input}!</h1>"
    return render_template_string(template)   # <-- SSTI risk

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)