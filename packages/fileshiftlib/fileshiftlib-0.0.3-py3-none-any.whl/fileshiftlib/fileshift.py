from dataclasses import dataclass
import logging
import paramiko


class SFTP(object):
    @dataclass
    class Configuration:
        host: str | None = None
        port: int | None = None
        username: str | None = None
        password: str | None = None

    def __init__(self, host: str, username: str, password: str, port: int = 22) -> None:
        """
        Initializes the SFTP client with the given configuration and authenticates.

        Args:
            host (str): The hostname of the SFTP server.
            username (str): The username for authentication.
            password (str): The password for authentication.
            port (int, optional): The port number of the SFTP server. Defaults to 22.
        """
        # Init logging
        self.__logger = logging.getLogger(name=__name__)
        self.__logger.setLevel(level=logging.INFO)
        handler = logging.StreamHandler()
        self.__logger.addHandler(handler)

        # Credentials/configuration
        self.sftp_client: paramiko.sftp_client.SFTPClient = None
        self.__transport: paramiko.transport.Transport = None

        self.__configuration = self.Configuration(host=host,
                                                  port=port,
                                                  username=username,
                                                  password=password)

        # Authenticate
        self.__transport, self.sftp_client = self.auth()

    def __del__(self) -> None:
        """
        Destructor to clean up the SFTP client and close the transport session.
        """
        self.__logger.info(msg="Closes session")

        self.__transport.close()
        self.sftp_client.close()

    def auth(self) -> tuple:
        """
        Authenticates with the SFTP server and initializes the SFTP client.

        Returns:
            tuple: A tuple containing the transport and SFTP client objects.
        """
        self.__logger.info(msg="Opens session")

        # Connect
        transport = paramiko.Transport((self.__configuration.host, self.__configuration.port))
        transport.connect(username=self.__configuration.username, password=self.__configuration.password)
        sftp_client = paramiko.SFTPClient.from_transport(transport)
        
        return transport, sftp_client
    
    def list_dir(self, path: str = ".") -> list:
        """
        Lists the names of the contents in the specified folder on the SFTP server.

        Args:
            path (str, optional): The path to the folder on the SFTP server. Defaults to the current directory.

        Returns:
            list: A list of names of the contents in the specified folder.
        """
        self.__logger.info(msg="Lists the names of the contents in the specified folder")
        self.__logger.info(msg=path)

        return self.sftp_client.listdir(path)

    def change_dir(self, path: str = ".") -> None:
        """
        Changes the current working directory on the SFTP server.

        Args:
            path (str, optional): The path to the folder to change to on the SFTP server. Defaults to the current directory.
        """
        self.__logger.info(msg="Changes the current working directory")
        self.__logger.info(msg=path)

        self.sftp_client.chdir(path)

    def delete_file(self, filename: str) -> None:
        """
        Deletes a file on the SFTP server.

        Args:
            filename (str): The name of the file to delete on the SFTP server.
        """
        self.__logger.info(msg="Deletes a file")
        self.__logger.info(msg=filename)

        self.sftp_client.remove(filename)

    def download_file(self, remote_path: str, local_path: str) -> None:
        """
        Downloads a file from the SFTP server to the local machine.

        Args:
            remote_path (str): The path to the file on the SFTP server.
            local_path (str): The path on the local machine where the file will be saved.
        """
        self.__logger.info(msg="Downloads a file from the SFTP server to the local machine")
        self.__logger.info(msg=remote_path)
        self.__logger.info(msg=local_path)

        self.sftp_client.get(remote_path, local_path)

    def upload_file(self, local_path: str, remote_path: str) -> None:
        """
        Uploads a file from the local machine to the SFTP server.

        Args:
            local_path (str): The path to the file on the local machine.
            remote_path (str): The path on the SFTP server where the file will be saved.
        """
        self.__logger.info(msg="Uploads a file from the local machine to the SFTP")
        self.__logger.info(msg=local_path)
        self.__logger.info(msg=remote_path)

        self.sftp_client.put(local_path, remote_path)

# eom
