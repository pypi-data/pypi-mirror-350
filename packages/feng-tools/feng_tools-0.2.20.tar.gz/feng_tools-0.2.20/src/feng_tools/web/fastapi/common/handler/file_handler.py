from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile
from starlette.requests import Request

from feng_tools.web.fastapi.common.schema.api_response import ApiResponse


class FileHandler(ABC):
    @abstractmethod
    def upload_handle(self, request:Request, file_type:str, file: UploadFile) -> ApiResponse:
        pass

    @abstractmethod
    def download_handle(self, request:Request, file_id:str, file_name:Optional[str]=None):
        pass
