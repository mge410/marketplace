import os
import uuid

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

from src.core.config import settings, Environment
from src.core.s3_client import S3Client

file_router = APIRouter(prefix="/files", tags=["files"])

def get_s3_client() -> S3Client:
    return S3Client()


@file_router.post("/upload")
async def upload_file(
        file: UploadFile,
        s3_client: S3Client = Depends(get_s3_client),
) -> JSONResponse:

    file_extension = os.path.splitext(file.filename)[1]
    object_name = f"{uuid.uuid4()}{file_extension}"
    temp_file_path = f"/tmp/{object_name}"

    try:
        contents = await file.read()
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        await s3_client.upload_file(temp_file_path)

        if settings.app.environment.value == Environment.DEV.value:
            file_url = f"{settings.s3_config.get_file_endpoint_url}/{s3_client.bucket_name}/{object_name}"
        else:
            file_url = f"https://{s3_client.bucket_name}.s3.{settings.s3_config.region_name}.amazonaws.com/{object_name}"

        os.remove(temp_file_path)

        return JSONResponse(
            content={
                "message": "File uploaded successfully",
                "url": file_url,
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )
