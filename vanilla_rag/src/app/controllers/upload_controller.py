# src/app/controllers/upload_controller.py

from fastapi import Depends, UploadFile

from ..usecases.upload_usecase import UploadUseCase


class UploadController:
    def __init__(self, upload_usecase: UploadUseCase = Depends()):
        self.upload_usecase = upload_usecase

    async def upload_file(self, file: UploadFile):
        return await self.upload_usecase.execute(file)
