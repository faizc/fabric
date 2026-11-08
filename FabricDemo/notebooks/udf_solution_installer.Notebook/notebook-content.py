# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse_name": "",
# META       "default_lakehouse_workspace_id": ""
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Unified Data Foundation with Fabric
# This notebook orchestrates the end-to-end deployment of **[Unified data foundation with Fabric solution accelerator](https://github.com/microsoft/unified-data-foundation-with-fabric-solution-accelerator/)** into the current Microsoft Fabric workspace using the [`fabric-launcher`](https://github.com/microsoft/fabric-launcher) library.
# 
# **Installation tasks**
# This notebook performs the following tasks:
# 1. **🚀 Deployment**: download source code, deploy Fabric items, load reference Data
# 1. **✅ Post-Deployment Tasks**: Complete post-deployment configuration tasks, such as:
#     - Import sample data
#     - Organize bronze data into silver data
#     - Organize silver data into gold data
# 
# **Expected duration**
# This notebook will take about 12 minutes to run

# MARKDOWN ********************

# ## 🚀 Deployment
# Download source code, deploy Fabric items, load sample data

# CELL ********************

%pip install fabric-launcher -U semantic-link --quiet
import notebookutils
notebookutils.session.restartPython()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

from fabric_launcher import FabricLauncher

launcher = FabricLauncher(notebookutils,
    api_root_url = "https://api.fabric.microsoft.com" #Default is https://api.fabric.microsoft.com, but may vary depending on your environment
    )


# ── GitHub source settings ────────────────────────────────────────────────────
GITHUB_OWNER     = "microsoft"
GITHUB_REPO      = "unified-data-foundation-with-fabric-solution-accelerator"
GITHUB_BRANCH    = "main"
GITHUB_UDF_WORKSPACE_PATH = "fabric_workspace"  # Folder inside the repo where UDF solution is synched
GITHUB_DATA_PATH = "infra/data"                 # Folder inside the repo containing the data to be ingested in the Lakehouse

# ── Fabric bronze Lakehouse target settings ─────────────────────────────────────────
LAKEHOUSE_BRONZE_NAME = "maag_bronze"      # Lakehouse in the workspace where the ingested CSV files will be landed
LAKEHOUSE_BRONZE_DATA_FOLDER  = "/"  # Root folder under Lakehouse Files/ where the ingested CSV files will be landed

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import traceback

try:
    # Deploy solution with data folders
    launcher.download_and_deploy(
        repo_owner=GITHUB_OWNER,
        repo_name=GITHUB_REPO,
        branch = GITHUB_BRANCH,
        workspace_folder=GITHUB_UDF_WORKSPACE_PATH,
        allow_non_empty_workspace=True,
        item_type_stages = [["Lakehouse"],["Notebook","Report","DataAgent","SemanticModel"]],
        validate_after_deployment=True,
        generate_report=False,
        data_folders={GITHUB_DATA_PATH: LAKEHOUSE_BRONZE_DATA_FOLDER},
        lakehouse_name=LAKEHOUSE_BRONZE_NAME
    )
except Exception as e:
    error_msg = f"Deployment FAILED: {type(e).__name__}: {e}"
    print(f"❌ {error_msg}")
    traceback.print_exc()
    notebookutils.notebook.exit(error_msg)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## ✅ Automated Post-Deployment Tasks

# CELL ********************

#Import required libraries
import sempy.fabric as fabric
from fabric_launcher import move_item_to_folder

# Initialize Fabric client and workspace
client = fabric.FabricRestClient()
workspace_id = fabric.get_workspace_id()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Run a notebook to: Convert and standardize data form Bronze to Silver Lakehouse
try:
    result = launcher.run_notebook_synchronous(
        notebook_name="run_bronze_to_silver",
        parameters={},
        timeout_seconds=3600
    )
except Exception as e:
    error_msg = f"run_bronze_to_silver FAILED: {type(e).__name__}: {e}"
    print(f"❌ {error_msg}")
    traceback.print_exc()
    notebookutils.notebook.exit(error_msg)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Run a notebook to: Segment data from Silver to Gold Lakehouse
try:
    result = launcher.run_notebook_synchronous(
        notebook_name="run_silver_to_gold",
        parameters={},
        timeout_seconds=3600
    )
except Exception as e:
    error_msg = f"run_silver_to_gold FAILED: {type(e).__name__}: {e}"
    print(f"❌ {error_msg}")
    traceback.print_exc()
    notebookutils.notebook.exit(error_msg)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Move current notebook to the Install folder
move_item_to_folder(
        item_name=notebookutils.runtime.context["currentNotebookName"],
        item_type="Notebook",
        folder_name="notebooks",
        workspace_id=workspace_id,
        client=client
    )
print("✅ Current notebook moved successfully!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Next Steps
# Your automated solution deployment is complete!
# 
# ⚠️ Please be sure to refresh your browser window to reflect all newly-deployed items in the Fabric portal!
# 
# Review the [README](https://github.com/microsoft/unified-data-foundation-with-fabric-solution-accelerator/?tab=readme-ov-file) document for details on running simulations and exploring your solution.
