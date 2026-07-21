import json
import sys
import os
import re

def transform_notebook(notebook_content, config):
    """
    Replace placeholders in notebook with environment-specific values
    Placeholders: {{CATALOG_NAME}}, {{SCHEMA_NAME}}, {{STORAGE_LOCATION}}, etc.
    """
    transformed = notebook_content
    
    replacements = {
        '{{CATALOG_NAME}}': config['unity_catalog']['catalog_name'],
        '{{SCHEMA_NAME}}': config['unity_catalog']['schema_name'],
        '{{STORAGE_LOCATION}}': config['unity_catalog']['storage_location'],
        '{{EXTERNAL_TABLE_PATH}}': config['unity_catalog']['external_table_path'],
        '{{NOTEBOOKS_PATH}}': config['paths']['notebooks_path'],
        '{{DATA_PATH}}': config['paths']['data_path'],
        '{{ENVIRONMENT}}': config['environment'],
    }
    
    for placeholder, value in replacements.items():
        transformed = transformed.replace(placeholder, value)
    
    return transformed

def process_notebooks(source_dir, target_dir, config):
    """Process all notebooks and apply environment-specific configurations"""
    os.makedirs(target_dir, exist_ok=True)
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.py'):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            
            with open(source_path, 'r') as f:
                content = f.read()
            
            transformed = transform_notebook(content, config)
            
            with open(target_path, 'w') as f:
                f.write(transformed)
            
            print(f"✓ Transformed {filename}")

if __name__ == '__main__':
    environment = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    
    # Load config
    with open(f'config/{environment}.json', 'r') as f:
        config = json.load(f)
    
    # Transform notebooks
    process_notebooks(
        f'notebooks/dev',
        f'notebooks/{environment}',
        config
    )
    
    print(f"✓ Configuration transformation completed for {environment}")
