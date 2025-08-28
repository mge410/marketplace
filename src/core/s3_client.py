from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional, TYPE_CHECKING

from aiobotocore.session import get_session
from aiobotocore.config import AioConfig

from src.core.config import settings, Environment

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client as BaseS3Client


class S3Client:
    def __init__(
        self,
        access_key: str = settings.s3_config.aws_access_key_id,
        secret_key: str = settings.s3_config.aws_secret_access_key,
        endpoint_url: str = str(settings.s3_config.put_file_endpoint_url),
        bucket_name: str = settings.s3_config.bucket_name,
        region_name: Optional[str] = settings.s3_config.region_name,
    ):
        self.config: Dict[str, Any] = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "region_name": region_name,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator["BaseS3Client", Any]:
        if settings.app.environment.value == Environment.DEV.value:
            s3_config = AioConfig(
                region_name=self.config["region_name"], s3={"addressing_style": "path"}
            )
        else:
            s3_config = AioConfig(s3={"addressing_style": "auto"})

        async with self.session.create_client(
            "s3",
            aws_access_key_id=self.config["aws_access_key_id"],
            aws_secret_access_key=self.config["aws_secret_access_key"],
            endpoint_url=self.config["endpoint_url"],
            config=s3_config,
        ) as client:
            yield client

    async def upload_file(self, file_path: str) -> None:
        object_name = file_path.split("/")[-1]
        async with self.get_client() as client:
            with open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )

    async def delete_file(self, object_name: str) -> None:
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_name)
