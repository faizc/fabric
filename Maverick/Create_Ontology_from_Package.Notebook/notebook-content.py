# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "afa3f146-b6f9-4553-8d87-69dab5531c39",
# META       "default_lakehouse_name": "lh_airlinedata",
# META       "default_lakehouse_workspace_id": "6ad1a698-5760-4d0f-9b06-68138ca66a9f",
# META       "known_lakehouses": [
# META         {
# META           "id": "afa3f146-b6f9-4553-8d87-69dab5531c39"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## Fabric IQ Accelerator Sample
#         
# ### Create Ontology from Package

# CELL ********************

# Install Fabric IQ Ontology Accelerator Package
%pip install /lakehouse/default/Files/fabriciq_ontology_accelerator-0.1.0-py3-none-any.whl --q

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import sempy.fabric as fabric
import json
from fabricontology import create_ontology_item, generate_definition_from_package

workspace_id = fabric.get_workspace_id()
access_token = notebookutils.credentials.getToken('pbi')

ontology_item_name = "AirlineOntology"
ontology_package_path = "/lakehouse/default/Files/airline_ontology_package.iq"

binding_lakehouse_name = "lh_airlinedata"
binding_lakehouse_schema_name = "dbo"  # replace this if using lakehouse without schemas
binding_eventhouse_name = "eh_airlinedata"
binding_eventhouse_cluster_uri = "https://trd-w7rq6k1va2aq6xh5e4.z7.kusto.fabric.microsoft.com"
binding_eventhouse_database_name = "eh_airlinedata"

items_df = fabric.list_items()
binding_lakehouse_item_id = str(items_df[(items_df["Type"] == "Lakehouse") & (items_df["Display Name"] == binding_lakehouse_name)].iloc[0].Id)
binding_eventhouse_item_id = str(items_df[(items_df["Type"] == "Eventhouse") & (items_df["Display Name"] == binding_eventhouse_name)].iloc[0].Id)
binding_workspace_id = workspace_id

ontology_definition, entity_types, relationship_types, data_bindings, contextualizations = generate_definition_from_package(
    ontology_package_path=ontology_package_path,
    ontology_name=ontology_item_name, 
    binding_workspace_id=binding_workspace_id,
    binding_lakehouse_item_id=binding_lakehouse_item_id,
    binding_lakehouse_schema_name=binding_lakehouse_schema_name,
    binding_eventhouse_item_id=binding_eventhouse_item_id,
    binding_eventhouse_cluster_uri=binding_eventhouse_cluster_uri,    
    binding_eventhouse_database_name=binding_eventhouse_database_name)

response = create_ontology_item(workspace_id=workspace_id, 
                           access_token=access_token,
                           ontology_item_name=ontology_item_name, 
                           ontology_definition=ontology_definition)
print(response.json())


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
