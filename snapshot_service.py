from datetime import datetime,timezone
from config import *
from email_service import EmailService

class SnapshotService:
    def __init__(self,compute_client):
        self.compute_client=compute_client
    
    def get_snapshot_deleted_data(self):
        virtual_machines=self.compute_client.virtual_machines.list(resource_group)
        email_obj=EmailService(email_address,email_password,lead_email)
        current_time=datetime.now(timezone.utc)
        deleted_snapshot=[]
        snapshots=self.compute_client.snapshots.list_by_resource_group(resource_group)
        for snapshot in snapshots:
            snapshot_name=snapshot.name
            creation_time=snapshot.time_created
            age_minutes=(current_time-creation_time).total_seconds()/60
            snapshot_disk=snapshot.creation_data.source_resource_id
            match_vm=None
            for vm in virtual_machines:
                if (vm.storage_profile.os_disk and vm.storage_profile.os_disk.managed_disk):
                    vm_disk=vm.storage_profile.os_disk.managed_disk.id
                    if vm_disk == snapshot_disk:
                        match_vm=vm
                        break
            if match_vm:
                tags=match_vm.tags
                if tags:
                    delete_snapshot=tags.get("delete_snapshot")
                    if (delete_snapshot=="true" and age_minutes > threshold_minutes):
                        delete_operation=self.compute_client.snapshots.begin_delete(
                            resource_group,snapshot_name
                        )
                        delete_operation.wait()
                        print(f"{snapshot_name} deleted Successfully")
                        deleted_snapshot.append({
                            "Snapshot Name": snapshot_name,
                            "Resource Group": resource_group,
                            "VM Name": match_vm.name,
                            "Created Time": str(creation_time),
                            "Deletion Time": str(current_time)
                        })
                        email_obj.send_email(snapshot_name,resource_group,match_vm.name)

        return deleted_snapshot

