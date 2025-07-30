# Sharepoint API
## Install
```bash
pip install sharepoint-api
```
## Setup Config
Create config.yaml
```yaml
TENANT_NAME: ""
SITE_NAME: ""
CLIENT_ID: "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxx"
CLIENT_SECRET: ""
LIBRARY_NAME: "Shared Documents"
```
Currently I am using Sharepoint "Shared Documents" area <br>
If you needs to change -> Change in YAML file
```yaml
LIBRARY_NAME: ""
``` 
## Examples:
```python
from sharepoint_api import SharePoint


sharepoint = SharePoint(config_path='config.yaml')
sp_path = "Myfiles/temp"
folder = sharepoint.get_folder(sp_path)
print(f"Folder: {folder}")
files, subfolders = sharepoint.list_folder_items()
print(files, subfolders)
# Download file
sharepoint.download_file(sp_path="Myfiles/temp/exam_result_v1.csv", local_file_path="/home/user/myfiles")

# Download Folder
sharepoint.download_folder(sp_path="Myfiles/temp/test1", local_file_path="/home/user/myfiles/sample")

# Upload File
sharepoint.upload_file("sample/exam_result_v1.csv", "Myfiles/temp/upload_test")

# Create Folder
sharepoint.create_folder("Myfiles/temp/test2")

# Delete Folder
sharepoint.delete_folder("Myfiles/temp/test2")

# Upload Folder
sharepoint.upload_folder("sample/test", "Myfiles/temp/CNH")
```