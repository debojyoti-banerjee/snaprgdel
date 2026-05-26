import smtplib
from email.mime.text import MIMEText
from datetime import datetime,timezone

class EmailService:
    def __init__(self,email_address,email_password,lead_email):
        self.email_address=email_address
        self.email_password=email_password
        self.lead_email=lead_email

    def send_email(self,snapshot_name,vm_name):
        subject=f"Snapshot Deletion Alert {snapshot_name}"
        body=f"""
        Snapshot Name: {snapshot_name}
        Resource Group: {resource_group}
        VM Name: {vm_name}
        Date of Deletion: {datetime.now(timezone.utc)}
        """
        message=MIMEText(body)
        message["Subject"]=subject
        message["To"]=self.lead_email
        message["From"]=self.email_address
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(self.email_address,self.email_password)
            server.send_message(message)
            print("Email send Successfully")