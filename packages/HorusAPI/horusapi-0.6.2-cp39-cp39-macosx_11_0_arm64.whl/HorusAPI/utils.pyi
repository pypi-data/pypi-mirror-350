import typing
from _typeshed import Incomplete

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.

    Intened for internal use only.
    """
    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """

class TempFile:
    """Temporary file class used to store temporary files in user dirs"""
    name: Incomplete
    tmpFolder: Incomplete
    path: Incomplete
    def __init__(self, name: str, folder: typing.Optional[str] = None) -> None:
        """
        - Name: The name of the file.
        - Folder: The folder where the file will be stored.
        If None, the file will bestored in the tmp folder.
        """
    def __eq__(self, other): ...
    def __hash__(self): ...
    def __del__(self) -> None: ...
    def delete(self) -> None:
        """
        Delete the file.
        """
    def write(self, content: str):
        """
        Write content to the file

        - content: The content to write to the file.
        """
    def read(self):
        """
        Read the content of the file

        :return: The content of the file as a string.
        """
    def deleteTmpFolder(self) -> None:
        """
        Deletes the tmp folder.
        """

def getUserFolder() -> str:
    """
    Returns the current logged in user's folder
    """

class ResetRemoteException(Exception):
    """
    Exception raised when the remote server is reset.
    """

def initPlugin() -> None:
    """
    This function will create the basic folder structure for building
    a Horus plugin.
    """
