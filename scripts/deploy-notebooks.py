import os
import json
import subprocess
import sys

def deploy_notebooks(environment):
    """Deploy Jupyter notebooks to Databricks workspace"""
    
    # Load environment config
    with open(f'config/{environment}.json', 'r') as f:
        config = json.load(f)
    
    host = config['workspace']['url']
    token = config['workspace']['token']
    notebooks_path = config['paths']['notebooks_path']
    
    # Get list of notebooks from HC_Azureproject folder
    notebook_dir = f'HC_Azureproject'
    
    if not os.path.exists(notebook_dir):
        print(f"✗ Notebook directory {notebook_dir} does not exist")
        sys.exit(1)
    
    for filename in os.listdir(notebook_dir):
        if filename.endswith('.ipynb'):
            notebook_path = os.path.join(notebook_dir, filename)
            # Remove .ipynb extension for remote path
            notebook_name = filename[:-6]
            remote_path = f'{notebooks_path}/{notebook_name}'
            
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
                # Continue with next notebook instead of exiting
    
    print(f"✓ Notebook deployment completed for {environment}")

if __name__ == '__main__':
    environment = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    deploy_notebooks(environment)
