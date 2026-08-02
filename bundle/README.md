# Declarative Automation Bundle notes

This bundle is intentionally deployment-only.

It does not create Databricks Jobs or Lakeflow Spark Declarative Pipelines because this project is orchestrated by Azure Data Factory (ADF), which calls Databricks notebooks directly.

What this bundle does:
- Deploys the HC_Azureporject notebooks and supporting config/scripts from this repository.
- Defines a dev target for the current workspace.
- Defines a prod target placeholder for a future production workspace.
- Keeps bundle-specific configuration separate from notebook business logic.

What you still need to do manually:
1. Create a production Databricks workspace.
2. Replace the prod target placeholders in bundle/targets.yml.
3. Create a production deployment identity (preferably a service principal) and token/OAuth setup.
4. Update ADF in each environment so notebook activities point to the deployed notebook paths in the target workspace.
5. Optionally externalize hardcoded environment-specific names from notebooks later; this bundle does not change notebook code.

Suggested commands:
- databricks bundle validate -t dev
- databricks bundle deploy -t dev
- databricks bundle validate -t prod
- databricks bundle deploy -t prod
