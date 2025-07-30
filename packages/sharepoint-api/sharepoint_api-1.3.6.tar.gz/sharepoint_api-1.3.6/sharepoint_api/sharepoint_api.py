import sys
import os
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
import yaml
from pathlib import Path


class SharePoint:
    def __init__(self, config_path:str):

        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        self.config = config
        self.TENANT_NAME = config['TENANT_NAME']
        self.SITE_NAME = config['SITE_NAME']
        self.CLIENT_ID = config['CLIENT_ID']
        self.CLIENT_SECRET = config['CLIENT_SECRET']
        # Example: https://<tenant_name>.sharepoint.com/sites/<site_name>
        self.SITE_URL = f"https://{self.TENANT_NAME}.sharepoint.com/sites/{self.SITE_NAME}"
        self.LIBRARY_NAME = config['LIBRARY_NAME']
        """
        Create and return a SharePoint ClientContext using the provided credentials.
        """
        credentials = ClientCredential(self.CLIENT_ID, self.CLIENT_SECRET)
        self.ctx = ClientContext(self.SITE_URL).with_credentials(credentials)
        
    
    def get_folder(self, sp_path):
        """
        Validate that the specified folder exists. Returns the folder if it exists,
        or None if it doesn't.
        """
        try:
            # if the "sp_path" send my windows OS system, it should be converted to Linux path format
            sp_path = sp_path.replace('\\', '/')
            folder_url = f"{self.LIBRARY_NAME}/{sp_path.strip('/')}"
            folder = self.ctx.web.get_folder_by_server_relative_url(folder_url)
            self.ctx.load(folder)
            self.ctx.execute_query()
            self.folder = folder
            return folder
        except Exception as e:
            # If there's an error (e.g., FileNotFoundError from SharePoint),
            # we treat the folder as invalid
            self.folder = None
            return None
        
    
    def list_folder_items(self):
        """
        Return separate lists of files and subfolders in the given SharePoint folder object.
        """
        # Get files
        folder_files = self.folder.files
        folder_folders = self.folder.folders
        #folder.folders.expand(["Name"]).get().execute_query()  # load subfolders
        self.ctx = self.folder.context

        self.ctx.load(folder_files)
        self.ctx.load(folder_folders)
        self.ctx.execute_query()

        files = [file.properties["Name"] for file in folder_files]
        subfolders = [subfold.properties["Name"] for subfold in folder_folders]

        return files, subfolders
    

    def print_download_progress(self, offset):
        # type: (int) -> None
        print("Downloaded '{0}' bytes...".format(offset))
    
    
    def download_file(self, sp_path, local_file_path):
        # if the "sp_path" send my windows OS system, it should be converted to Linux path format
        sp_path = sp_path.replace('\\', '/')
        """
        Downloads a single file from SharePoint at server_relative_file_url to local_file_path.
        """
        file_url = f"{self.LIBRARY_NAME}/{sp_path.strip('/')}"
        source_file = self.ctx.web.get_file_by_server_relative_path(file_url)
        linux_path_list = os.path.split(file_url)[1].split('/')
        full_local_path = os.path.join(local_file_path, str(Path(*linux_path_list)))
        with open(full_local_path, "wb") as local_file:
            source_file.download_session(local_file, self.print_download_progress).execute_query()
        print(f"[SUCCESS] [Downloaded] {file_url} -> {full_local_path}")
    
    
    def download_folder(self, sp_path, local_file_path):
        # if the "sp_path" send my windows OS system, it should be converted to Linux path format
        sp_path = sp_path.replace('\\', '/')
        folder = self.get_folder(sp_path)
        if folder is None:
            print(f"[ERROR]: The path '{sp_path}' is not a valid SharePoint folder.")
            sys.exit(1)
    
        print(f"[SUCESS] Located: {folder}")
        folder_name = sp_path.split('/')[-1]
        path_to_save = os.path.join(local_file_path, folder_name)
        os.makedirs(path_to_save, exist_ok=True)
        files, subfolders = self.list_folder_items()
        for file in files:
            self.download_file(sp_path=f"{sp_path}/{file}", local_file_path=path_to_save)
        for subfolder in subfolders:
            self.download_folder(sp_path=f"{sp_path}/{subfolder}", local_file_path=os.path.join(local_file_path, folder_name))

    
    def upload_file(self, local_path, sp_path, size_chunk=1000000):
        def print_upload_progress(offset):
            # type: (int) -> None
            file_size = os.path.getsize(local_path)
            print(
                "Uploaded '{0}' bytes from '{1}'...[{2}%]".format(
                    offset, file_size, round(offset / file_size * 100, 2)
                )
            )
        # if the "sp_path" send my windows OS system, it should be converted to Linux path format
        sp_path = sp_path.replace('\\', '/')
        target_url = os.path.join(self.LIBRARY_NAME, sp_path.strip('/'))
        target_folder = self.ctx.web.get_folder_by_server_relative_url(target_url)
        with open(local_path, "rb") as f:
            uploaded_file = target_folder.files.create_upload_session(
                f, size_chunk, print_upload_progress
            ).execute_query()

        print(f"[SUCCESS] [UPLOADED] {local_path} -> {uploaded_file.serverRelativeUrl}")

    
    def create_folder(self, folder_url:str):
        # if the URL send my windows OS system, it should be converted to Linux path format
        folder_url = folder_url.replace('\\', '/')
        ffolder_url = f"{self.LIBRARY_NAME}/{folder_url.strip('/')}"
        folder = (
            self.ctx.web.ensure_folder_path(ffolder_url)
            .get()
            .select(["ServerRelativePath"])
            .execute_query()
        )
        print(f"[SUCCESS] [CREATED] {folder.server_relative_path}")

    
    def delete_folder(self, folder_url):
        folder = self.get_folder(folder_url)
        folder.delete_object().execute_query()
        print(f"Folder {folder_url} has been deleted")

    
    def delete_file(self, file_url):
        # if the URL send my windows OS system, it should be converted to Linux path format
        file_url = file_url.replace('\\', '/')
        target_url = f"{self.LIBRARY_NAME}/{file_url.strip('/')}"
        file = self.ctx.web.get_file_by_server_relative_path(target_url)
        file.delete_object().execute_query()
        print(f"File {file_url} has been deleted")


    def upload_folder(self, local_file_path, sp_path, size_chunk=1000000):
        len_dir = len(Path(local_file_path).parts)
        for dirpath, dirnames, filenames in os.walk(local_file_path):
            # print(dirpath, dirnames, filenames)
            dir_path_list = Path(dirpath).parts[len_dir-1:]
            # print(dir_path_list)
            # dir_path = str(Path(*dir_path_list))
            dir_path = '/'.join(dir_path_list)
            # print(dir_path)
            self.create_folder(f"{sp_path}/{dir_path}")
            for filename in filenames:
                self.upload_file(os.path.join(dirpath, filename), f"{sp_path}/{dir_path}", size_chunk)

