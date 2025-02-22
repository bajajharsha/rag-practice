# src/app/routes/upload_routes.py

from fastapi import APIRouter, Depends, UploadFile

from ..controllers.upload_controller import UploadController

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile, upload_controller: UploadController = Depends()
):
    return await upload_controller.upload_file(file)
