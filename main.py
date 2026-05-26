import pandas as pd
from config import *
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.blob import BlobServiceClient
from snapshot_service import SnapshotService
from storage_service import StorageService


credential=DefaultAzureCredential()
compute_client=ComputeManagementClient(credential,subscription_id)
blob_service_client=BlobServiceClient.from_connection_string(connection_string)
container_client=blob_service_client.get_container_client(container_name)
blob_client=container_client.get_blob_client(blob_name)


snapshot_obj=SnapshotService(compute_client)
storage_obj=StorageService(blob_client,excel_file)


deleted_snapshot_data=snapshot_obj.get_snapshot_deleted_data()
new_dataframe=pd.DataFrame(deleted_snapshot_data)
if (new_dataframe.empty==False):
    old_dataframe=storage_obj.download_excel()
    final_dataframe=pd.concat([old_dataframe,new_dataframe],ignore_index=True)
    storage_obj.upload_excel(final_dataframe)




