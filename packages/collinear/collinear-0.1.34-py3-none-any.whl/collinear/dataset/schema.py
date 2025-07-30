from pydantic import BaseModel, Field
from typing import Optional
import uuid

class ConversationMessage(BaseModel):
    role: str
    content: str

class DatasetAnnotationsRequestDTO(BaseModel):
    conv_prefix: list[ConversationMessage]
    response: str
    judgements: object = {}
    ground_truth: Optional[int] = None


class CreateNewDatasetRequestDTO(BaseModel):
    name: str
    space_id: uuid.UUID
    parent_dataset_id: Optional[uuid.UUID] = None
    conversations: list[DatasetAnnotationsRequestDTO]

class CreateNewDatasetRequestDTO(BaseModel):
    name: str = Field(..., example="Test_Dataset_001")
    space_id: uuid.UUID = Field(..., example="ac5b59fe-f9e6-404a-97df-972c2390948f")
    parent_dataset_id: Optional[uuid.UUID] = Field(None, example="add_if_available")
    conversations: list[DatasetAnnotationsRequestDTO] = Field(
        ..., example=[
            {
                "conv_prefix": [
                    {"role": "user", "content": "You are a helpful assistant."}
                ],
                "response": "Hello! How can I help you today?",
                "judgements": {"coherence": 4, "relevance": 5},
                "ground_truth": 1
            },
            {
                "conv_prefix": [
                    {"role": "user", "content": "Tell me a joke."}
                ],
                "response": "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "judgements": {"humor": 5},
                "ground_truth": 1
            },
            {
                "conv_prefix": [
                    {"role": "assistant", "content": "Why did the scarecrow win an award? Because he was outstanding in his field!"}
                ],
                "response": "",
                "judgements": {},
                "ground_truth": 1
            }
        ]
    )
