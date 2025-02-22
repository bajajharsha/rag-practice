# src/app/usecases/upload_usecase.py

from fastapi import Depends, UploadFile

from ..services.upload_service import UploadService


class UploadUseCase:
    def __init__(self, upload_service: UploadService = Depends()):
        self.upload_service = upload_service

    async def execute(self, file: UploadFile):
        """Executes the upload and processing flow."""
        return await self.upload_service.process_upload(file)
