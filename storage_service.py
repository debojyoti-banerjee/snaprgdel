import pandas as pd

class StorageService:
    def __init__(self,blob_client,excel_file):
        self.blob_client=blob_client
        self.excel_file=excel_file
    
    def download_excel(self):
        try:
            download_stream=blob_client.download_blob()
            with open(self.excel_file,"wb") as f:
                f.write(download_stream.readall())
            old_dataframe=pd.read_excel(self.excel_file,engine="openpyxl")
            print("Old Excel file Downloaded")
            return old_dataframe
        except Exception:
            print("No existing Excel file exist")
            old_dataframe=pd.DataFrame()
            return old_dataframe

    def upload_excel(self,dataframe):
        dataframe.to_excel(self.excel_file,index=False,engine="openpyxl")
        with open(self.excel_file,"rb") as f:
            self.blob_client.upload_blob(f,overwrite=True)
        print("Excel File uploaded successfully")

