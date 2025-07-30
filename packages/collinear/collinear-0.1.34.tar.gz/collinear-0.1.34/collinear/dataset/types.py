import uuid

from pydantic import BaseModel


class UploadDatasetResponseType(BaseModel):
    dataset_id: str
    dataset: list[dict]

class CreateDatasetResponseType(BaseModel):
    message: str
    dataset_id: str
