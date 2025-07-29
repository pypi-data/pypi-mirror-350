
import os
from datetime import datetime
from ftplib import FTP
from pathlib import Path
from typing import List, Optional

from dateutil import parser

from vito.sas.air import logger


def path_to_string(path:Path, sep='/'):
    """
    Args:
        path: The Path instance
        sep: Path seperator ('/' by default)

    Returns: String representation of the path with the specified separator.
    """
    str_path = str(path)
    if sep != os.sep:
        str_path = str_path.replace(os.sep, sep)
    return str_path


class FtpIO:
    """
    Class to manage files on a remote server with FTP.
    """

    def __init__(self, hostname: str, port=21, encoding="utf-8"):
        self.host = hostname
        self.port = port
        self.encoding = encoding
        self.ftp_client = None

    def __call__(self, **kwargs) -> 'FtpIO':
        if 'pw' in kwargs and 'user' in kwargs:
            self.ftp_client = FTP(host=self.host, encoding=self.encoding)
            self.ftp_client.port = self.port
            logger.info("LOGIN ftp")
            self.ftp_client.login(user=kwargs['user'], passwd=kwargs['pw'])
        return self

    def __enter__(self, **kwargs) -> 'FtpIO':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Will close the SSH connection.
        """
        if self.ftp_client is not None:
            logger.info("QUIT ftp")
            self.ftp_client.quit()
            self.ftp_client = None

    def download_files(self, remote_dir: Path, local_dir: Path):
        local_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Download folder: {local_dir.absolute()}")
        self.ftp_client.cwd(path_to_string(remote_dir))
        for file in self.ftp_client.nlst():
            local_file = Path(local_dir, file)
            with open(local_file, "wb") as ofile:
                ftp_cmd = f"RETR {file}"
                logger.info(ftp_cmd)
                self.ftp_client.retrbinary(ftp_cmd, ofile.write)

    def download_file(self, remote_file: Path, local_dir: Path):
        local_dir.mkdir(parents=True, exist_ok=True)
        self.ftp_client.cwd(path_to_string(remote_file.parent))
        file_name = remote_file.name
        with open(Path(local_dir, file_name), "wb") as ofile:
            ftp_cmd = f"RETR {file_name}"
            logger.info(f"DOWNLOAD {path_to_string(remote_file)} to {local_dir}")
            self.ftp_client.retrbinary(ftp_cmd, ofile.write)

    def clear_folder(self, remote_dir: Path):
        self.ftp_client.cwd(remote_dir)
        for file in self.ftp_client.nlst():
            logger.info(f"DELETE {path_to_string(Path(remote_dir, file))}")
            self.ftp_client.delete(file)

    def delete_file(self, remote_file: Path):
        logger.info(f"DELETE {path_to_string(remote_file)}")
        self.ftp_client.cwd(path_to_string(remote_file.parent))
        self.ftp_client.delete(remote_file.name)

    def modified(self, remote_file: Path) -> Optional[datetime]:
        path_remote_file = path_to_string(remote_file)
        try:
            timestamp = self.ftp_client.voidcmd(f"MDTM {path_remote_file}")[4:].strip()
            return parser.parse(timestamp)
        except Exception as e:
            logger.error(f"Error getting modified time for {path_remote_file}: {e}")
            return None

    def list_files(self, remote_dir: Path) -> List[str]:
        self.ftp_client.cwd(path_to_string(remote_dir))
        try:
            return self.ftp_client.nlst()
        except Exception as e:
            logger.error(f"Error listing files in {path_to_string(remote_dir)}: {e}")
            return []


# class SftpIO:
#     """
#     Class to manage files on a remote server with SSH (sftp sessions).
#     """
#
#     def __init__(self, host, username, port=22):
#         self.host = host
#         self.username = username
#         self.port = port
#
#     def __call__(self, **kwargs):
#         if 'pw' in kwargs.keys():
#             import paramiko
#             self.ssh_client = paramiko.SSHClient()
#             self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             self.ssh_client.connect(self.host, self.port, self.username, kwargs['pw'])
#         return self
#
#     def __enter__(self, **kwargs):
#         # self.ssh_client = paramiko.SSHClient()
#         # self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         # self.ssh_client.connect(self.host, self.port, self.username, '')
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb ):
#         self.close()
#
#     def close(self):
#         """
#         Will close the SSH connection.
#         """
#         if self.ssh_client:
#             self.ssh_client.close()
#             del self.ssh_client
#
#     def send_file_to_server(self, input_file, store_name):
#         """
#         Will send a local file to the remote server.
#         Args:
#             input_file: Path to local file
#             remote_path: Destination folder on the remote server.
#             destination_file: Filename of the file that will be created on the remote server.
#         """
#         input_file = str(input_file)
#         remote_path = str(Cfg.vars().geoserver.remote_folder)
#         destination_file = pu.path_to_string(pu.to_path(remote_path,str(store_name),os.path.basename(input_file)))
#         with self.ssh_client.open_sftp() as sftp:
#             try:
#                 sftp.chdir(os.path.dirname(destination_file))  # Test if remote_path exists
#             except IOError:
#                 sftp.mkdir(os.path.dirname(destination_file))  # Create remote_path
#             sftp.put(input_file, destination_file)
#             return destination_file
#
#     def delete_file_from_server(self, remote_path, file_name):
#         """
#         Will remove a file from the remote server.
#         Args:
#             remote_path: Directory of the file on the remote server that will be deleted.
#             file_name: Name of the file that will be deleted.
#         """
#         remote_path = str(remote_path)
#         file_name = str(file_name)
#         with self.ssh_client.open_sftp() as sftp:
#             try:
#                 sftp.chdir(remote_path)  # Test if remote_path exists
#             except IOError:
#                 return f'Path {remote_path} does not exist.'
#             return sftp.remove(file_name)
#
#
#
# class AwsIO:
#     """
#     Class to manage files on an AWS bucket.
#     """
#
#     def __init__(self, bucket):
#         self.bucket_name = bucket
#
#     def __call__(self, access_key, secret_key, **kwargs):
#         import boto3
#
#         logger.info(f"AwsIO __call__() kwargs: {kwargs}")
#         self.s3_resource = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, **kwargs)
#         return self
#
#     def __enter__(self, **kwargs):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb ):
#         # self.close()
#         pass
#
#     def delete_file_from_server(self, remote_path, file_name):
#         """
#         Will remove a file from the remote server.
#         Args:
#             remote_path: Directory of the file on the remote server that will be deleted.
#             file_name: Name of the file that will be deleted.
#         """
#         remote_path = str(remote_path).strip('/')
#         file_name = str(file_name).strip('/')
#
#         bucket = self.s3_resource.Bucket(self.bucket_name)
#         file_key = f"{remote_path}/{file_name}"
#
#         response = bucket.Object(file_key).delete()
#         print(response)
#
#     def send_file_to_server(self, input_file, remote_path):
#         """
#         Will send a local file to the remote server.
#         Args:
#             input_file: Path to local file
#             remote_path: Destination folder and filename on the bucket.
#         """
#         bucket = self.s3_resource.Bucket(self.bucket_name)
#         response = bucket.upload_file(str(input_file), str(remote_path))
#         print(response)
#
#     def list_files(self, remote_dir: Path) -> List[str]:
#         """
#         Will return the content of the remote directory
#         Args:
#             remote_dir:
#         """
#         bucket = self.s3_resource.Bucket(self.bucket_name)
#         # keys = [my_bucket_object.key  for my_bucket_object in bucket.objects.all()]
#         keys = [my_bucket_object.key for my_bucket_object in bucket.objects.filter(Prefix=str(remote_dir))]
#         return keys
#
#     def download_file(self, remote_file: Path, local_dir: Path):
#         """
#         Will download a remote file to a local directory
#         Args:
#             remote_file:
#             local_dir:
#         """
#         bucket = self.s3_resource.Bucket(self.bucket_name)
#         file_name = remote_file.name
#         key = str(remote_file)
#         bucket.download_file(key, str(Path(local_dir, file_name)))
