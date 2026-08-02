# Azure Human Capital - PWC

This repository contains the Databricks notebooks and CI/CD configuration for deploying data pipelines across Dev and Production environments.

## Project Structure

```
azurehumancapitalpwc/
├── .github/workflows/
│   ├── deploy-dev.yml          # Dev deployment workflow
│   └── deploy-prod.yml         # Production deployment workflow
├── config/
│   ├── config-template.json    # Configuration template
│   ├── dev.json               # ⚠️ EDIT: Dev environment config
│   └── prod.json              # ⚠️ EDIT: Prod environment config
├── notebooks/
│   ├── dev/
│   │   ├── unity_catalog_ddl.py      # Unity Catalog DDL with placeholders
│   │   ├── data_pipeline.py          # Data pipeline notebook
│   │   └── transformations.py        # Transformation notebook
│   ├── prod/                         # Auto-generated from dev with prod config
│   └── shared/
│       └── common_utilities.py       # Shared utilities
├── scripts/
│   ├── transform-config.py    # Transforms dev notebooks to env-specific versions
│   ├── deploy-notebooks.py    # Deploys notebooks to Databricks
│   └── deploy-unity-catalog.py # Deploys Unity Catalog DDL
└── README.md
```

## 🔧 Files You Need to Edit

### 1. **config/dev.json** ⚠️ REQUIRED

Update with your actual Dev environment details:

```json
{
  "workspace": {
    "url": "https://adb-xxx.azuredatabricks.net",  // Your Dev Databricks URL
    "token": "${DATABRICKS_DEV_TOKEN}"
  },
  "unity_catalog": {
    "catalog_name": "dev_catalog",  // Your dev catalog name
    "schema_name": "dev_schema",    // Your dev schema name
    "storage_location": "abfss://dev-container@devstorage.dfs.core.windows.net/data",  // Your dev storage
    "external_table_path": "abfss://dev-container@devstorage.dfs.core.windows.net/external-tables"
  },
  "paths": {
    "notebooks_path": "/Workspace/Users/dev",  // Your dev notebooks path
    "data_path": "abfss://dev-data@devstorage.dfs.core.windows.net"
  }
}
```

### 2. **config/prod.json** ⚠️ REQUIRED

Update with your actual Production environment details:

```json
{
  "workspace": {
    "url": "https://adb-yyy.azuredatabricks.net",  // Your Prod Databricks URL
    "token": "${DATABRICKS_PROD_TOKEN}"
  },
  "unity_catalog": {
    "catalog_name": "prod_catalog",  // Your prod catalog name
    "schema_name": "prod_schema",    // Your prod schema name
    "storage_location": "abfss://prod-container@prodstorage.dfs.core.windows.net/data",  // Your prod storage
    "external_table_path": "abfss://prod-container@prodstorage.dfs.core.windows.net/external-tables"
  },
  "paths": {
    "notebooks_path": "/Workspace/Users/prod",  // Your prod notebooks path
    "data_path": "abfss://prod-data@prodstorage.dfs.core.windows.net"
  }
}
```

### 3. **notebooks/dev/unity_catalog_ddl.py** ⚠️ EDIT - Add Your DDL

Replace the sample DDL with your actual DDL statements. Keep the placeholders:
- `{{CATALOG_NAME}}` - Will be replaced automatically
- `{{SCHEMA_NAME}}` - Will be replaced automatically
- `{{STORAGE_LOCATION}}` - Will be replaced automatically
- `{{EXTERNAL_TABLE_PATH}}` - Will be replaced automatically
- `{{ENVIRONMENT}}` - Will be replaced automatically

### 4. **notebooks/dev/data_pipeline.py** ⚠️ EDIT - Add Your Pipeline Logic

Replace with your actual data pipeline code.

### 5. **notebooks/dev/transformations.py** ⚠️ EDIT - Add Your Transformations

Replace with your actual transformation logic.

## 🔐 GitHub Secrets Setup

Go to **Settings → Secrets and variables → Actions** and add:

```
DATABRICKS_DEV_HOST=https://adb-xxx.azuredatabricks.net
DATABRICKS_DEV_TOKEN=dapi...xxxxx
DATABRICKS_PROD_HOST=https://adb-yyy.azuredatabricks.net
DATABRICKS_PROD_TOKEN=dapi...yyyyy
```

## 📋 How to Get Databricks Tokens

1. Go to Databricks workspace
2. Click on your profile icon (top right)
3. Select "Settings"
4. Go to "Developer" tab
5. Click "Generate new token"
6. Copy the token and paste in GitHub Secrets

## 🚀 Workflow

### Development Workflow

```bash
# 1. Clone repo
git clone https://github.com/junaid20950/azurehumancapitalpwc.git
cd azurehumancapitalpwc

# 2. Create dev branch (already created)
git checkout dev

# 3. Add your notebooks to notebooks/dev/ directory
# Edit config/dev.json with your Dev details

# 4. Commit and push
git add .
git commit -m "Add dev notebooks and config"
git push origin dev

# GitHub Actions automatically:
# - Transforms notebooks using dev config
# - Deploys to Dev Databricks workspace
```

### Production Deployment

```bash
# 1. Create a Pull Request: dev → main
git checkout main
git pull origin main
git merge dev

# 2. Review PR and merge to main
git push origin main

# GitHub Actions automatically:
# - Transforms notebooks using prod config
# - Changes all {{PLACEHOLDER}} to prod values
# - Deploys to Prod Databricks workspace
```

## 🔄 How Configuration Transformation Works

**Example:** Your dev notebook has:
```python
catalog = "{{CATALOG_NAME}}"
storage = "{{STORAGE_LOCATION}}"
```

**For Dev (dev.json):**
- `{{CATALOG_NAME}}` → `dev_catalog`
- `{{STORAGE_LOCATION}}` → `abfss://dev-container@devstorage.dfs.core.windows.net/data`

**For Prod (prod.json):**
- `{{CATALOG_NAME}}` → `prod_catalog`
- `{{STORAGE_LOCATION}}` → `abfss://prod-container@prodstorage.dfs.core.windows.net/data`

**No manual editing needed!** The transformation script does it automatically.

## 📝 Available Placeholders

Use these in your notebooks:

| Placeholder | Example Value |
|------------|---------------:|
| `{{CATALOG_NAME}}` | `dev_catalog` or `prod_catalog` |
| `{{SCHEMA_NAME}}` | `dev_schema` or `prod_schema` |
| `{{STORAGE_LOCATION}}` | `abfss://container@storage.dfs.core.windows.net/data` |
| `{{EXTERNAL_TABLE_PATH}}` | `abfss://container@storage.dfs.core.windows.net/external-tables` |
| `{{NOTEBOOKS_PATH}}` | `/Workspace/Users/dev` or `/Workspace/Users/prod` |
| `{{DATA_PATH}}` | `abfss://data@storage.dfs.core.windows.net` |
| `{{ENVIRONMENT}}` | `dev` or `prod` |

## ✅ Testing

### Test Dev Deployment

1. Edit config/dev.json with your actual dev environment
2. Add test notebooks to notebooks/dev/
3. Push to dev branch
4. Check GitHub Actions → Workflows → Deploy to Development

### Test Prod Deployment

1. Edit config/prod.json with your actual prod environment
2. Create a PR from dev → main
3. Merge to main
4. Check GitHub Actions → Workflows → Deploy to Production

## 🐛 Troubleshooting

### Workflow fails with "token not found"
- Check GitHub Secrets are set correctly
- Verify DATABRICKS_DEV_HOST and DATABRICKS_DEV_TOKEN exist

### Notebooks not deploying
- Ensure notebooks/dev/ folder exists with .py files
- Check Python scripts have proper permissions
- Verify notebook paths in config files are correct

### Transformation not working
- Ensure placeholders are in correct format: `{{PLACEHOLDER_NAME}}`
- Check config files have valid JSON syntax

## 📚 References

- [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Databricks Unity Catalog](https://docs.databricks.com/en/data-governance/unity-catalog/)

## 📧 Support

For questions or issues, create a GitHub issue in this repository.
