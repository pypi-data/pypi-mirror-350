import os
import os.path as op
import shutil
from typing import Callable

from fastapi import UploadFile

from .setting import Setting
from .utils import secure_filename, uuid_namegen

__all__ = ["FileManager"]


class FileManager:
    base_path: str = None
    relative_path: str = ""
    allowed_extensions: list[str] = None
    namegen: Callable[[UploadFile], str] = None
    permission = 0o755

    def __init__(
        self,
        base_path: str | None = None,
        relative_path: str = "",
        allowed_extensions: list[str] | None = None,
        namegen: Callable[[UploadFile], str] | None = None,
        permission: int | None = None,
        **kwargs,
    ):
        self.base_path = base_path or Setting.UPLOAD_FOLDER
        self.relative_path = relative_path
        self.allowed_extensions = allowed_extensions or Setting.FILE_ALLOWED_EXTENSIONS
        self.namegen = namegen or uuid_namegen
        self.permission = permission or self.permission

        if not self.base_path:
            raise Exception("UPLOAD_FOLDER not set in config.")

    def is_file_allowed(self, filename: str) -> bool:
        """
        Check if a file is allowed based on its extension.

        Args:
            filename (str): The name of the file.

        Returns:
            bool: True if the file is allowed, False otherwise.
        """
        if not self.allowed_extensions:
            return True

        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions
        )

    def generate_name(self, file_data: UploadFile) -> str:
        """
        Generates a name for the given file data.

        Args:
            file_data (UploadFile): The file data to generate a name for.

        Returns:
            str: The generated name for the file.
        """
        return self.namegen(file_data)

    def get_path(self, filename: str) -> str:
        """
        Returns the full path of a file by joining the base path with the given filename.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The full path of the file.
        """
        return op.join(self.base_path, filename)

    def delete_file(self, filename: str) -> None:
        """
        Deletes a file from the file system.

        Args:
            filename (str): The name of the file to delete.

        Returns:
            None
        """
        path = self.get_path(filename)
        if op.exists(path):
            os.remove(path)

    def save_file(self, file_data: UploadFile, filename: str) -> str:
        """
        Saves a file to the file system.

        Args:
            file_data (UploadFile): The file data to save.

        Returns:
            str: The name of the saved file.
        """
        secured_filename, path = self.generate_secure_filename(filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file_data.file, buffer)
        return secured_filename

    def save_content_to_file(self, content: bytes, filename: str) -> str:
        """
        Saves content to a file.

        Args:
            content (bytes): The content to save.
            filename (str): The name of the file.

        Returns:
            str: The name of the saved file.
        """
        secured_filename, path = self.generate_secure_filename(filename)
        with open(path, "wb") as buffer:
            buffer.write(content)
        return secured_filename

    def generate_secure_filename(self, filename):
        """
        Generates a secure filename by using the `secure_filename` function from the Werkzeug library.

        Also creates the directory where the file will be saved if it doesn't exist.

        Args:
            filename (str): The original filename.

        Returns:
            tuple: A tuple containing the secured filename and the path where the file will be saved.
        """
        secured_filename = secure_filename(filename)
        path = self.get_path(secured_filename)
        if not op.exists(op.dirname(path)):
            os.makedirs(os.path.dirname(path), self.permission)
        return secured_filename, path
