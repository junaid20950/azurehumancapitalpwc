import os
import json
import subprocess
import sys

def deploy_notebooks(environment):
    """Deploy notebooks to Databricks workspace"""
    
    # Load environment config
    with open(f'config/{environment}.json', 'r') as f:
        config = json.load(f)
    
    host = config['workspace']['url']
    token = config['workspace']['token']
    notebooks_path = config['paths']['notebooks_path']
    
    # Get list of transformed notebooks
    notebook_dir = f'notebooks/{environment}'
    
    if not os.path.exists(notebook_dir):
        print(f"✗ Notebook directory {notebook_dir} does not exist")
        sys.exit(1)
    
    for filename in os.listdir(notebook_dir):
        if filename.endswith('.py'):
            notebook_path = os.path.join(notebook_dir, filename)
            remote_path = f'{notebooks_path}/{filename[:-3]}'  # Remove .py extension
            
            # Deploy using databricks-cli
            cmd = [
                'databricks', 'workspace', 'import',
                notebook_path,
                remote_path,
                '--language', 'PYTHON',
                '--overwrite'
            ]
            
            env = os.environ.copy()
            env['DATABRICKS_HOST'] = host
            env['DATABRICKS_TOKEN'] = token
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ Deployed {filename} to {remote_path}")
            else:
                print(f"✗ Failed to deploy {filename}: {result.stderr}")
                sys.exit(1)

if __name__ == '__main__':
    environment = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    deploy_notebooks(environment)
