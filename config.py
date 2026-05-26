import os

subscription_id=os.environ["SUBSCRIPTION_ID"]
resource_group=os.environ["RESOURCE_GROUP"]
threshold_minutes=int(os.environ["THRESHOLD_MINUTES"])
connection_string=os.environ["AZURE_STORAGE_CONNECTION_STRING"]
email_address=os.environ["EMAIL_ADDRESS"]
email_password=os.environ["EMAIL_PASSWORD"]
lead_email=os.environ["LEAD_EMAIL"]

container_name="reports"
blob_name="deleted_snapshot.xlsx"
excel_file="deleted_snapshot.xlsx"