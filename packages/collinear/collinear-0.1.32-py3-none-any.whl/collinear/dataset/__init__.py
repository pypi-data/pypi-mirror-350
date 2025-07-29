import json
import uuid
from pathlib import Path
import aiohttp
import pandas as pd

from collinear.BaseService import BaseService
from collinear.dataset.types import UploadDatasetResponseType


class Dataset(BaseService):
    def __init__(self, access_token: str, space_id: str) -> None:
        super().__init__(access_token, space_id)

    async def upload_dataset(self, data: pd.DataFrame,
                             conv_prefix_column_name: str,
                             response_column_name: str,
                             context_column_name: str|None,
                             ground_truth_column_name: str | None,
                             dataset_name: str) -> UploadDatasetResponseType:
        """
        Uploads a dataset to the Collinear platform.
        Args:
            data: A pandas DataFrame containing the dataset.
            conv_prefix_column_name: Name of the column containing the conversation prefix.
            response_column_name: Name of the column containing the response.
            ground_truth_column_name: Name of the column containing the ground truth. If not provided, the column will be ignored.
            context_column_name: Name of the column containing the context. If not provided, the column will be ignored.
            dataset_name: Name of the dataset.

        Returns:
            UploadDatasetResponseType: ID of the uploaded dataset and rows.
        """

        conversations = []
        for _, row in data.iterrows():
            obj = {
                'conv_prefix': list(row[conv_prefix_column_name]),
                'response': row[response_column_name],
                'ground_truth': row[
                    ground_truth_column_name] if ground_truth_column_name and ground_truth_column_name in row else {},
                'context': row[context_column_name] if context_column_name and context_column_name in row else None
            }
            conversations.append(obj)
        json_file_name = "dataset.json"
        with open(json_file_name, "w") as json_file:
            json.dump(conversations, json_file)
        with open(json_file_name, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file, filename=json_file_name, content_type='application/json')
            form_data.add_field('dataset_name', dataset_name)
            resp = await self.send_form_request('/api/v1/dataset/upload', form_data, "POST")
            return UploadDatasetResponseType(dataset_id=resp['data_id'], dataset=resp['data'])

    async def upload_assessed_dataset(self, data: pd.DataFrame,
                                      evaluation_name: str,
                                      dataset_id: str) -> str:
        """
        Uploads a dataset to the Collinear platform.
        Args:
            data: A pandas DataFrame containing the dataset.
            evaluation_name: Name of the evaluation.
            dataset_id: ID of the dataset.

        Returns:
            dataset_id: ID of the uploaded dataset.
        """

        conversations = []
        for _, row in data.iterrows():
            obj = {
                'id': row['id'],
                'judgement': row['judgement']
            }
            conversations.append(obj)
        json_file_name = "dataset.json"
        with open(json_file_name, "w") as json_file:
            json.dump(conversations, json_file)
        with open(json_file_name, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file, filename=json_file_name, content_type='application/json')
            form_data.add_field('evaluation_name', evaluation_name)
            form_data.add_field('dataset_id', dataset_id)
            resp = await self.send_form_request('/api/v1/dataset/assess/upload', form_data, "POST")
            return resp['data']['data']['evaluation_id']
    

    async def upload_conversation_dataset(self,
                                          file_path: str,
                                          dataset_name: str,
                                          customer_message_column_name: str,
                                          agent_reply_column_name: str) -> UploadDatasetResponseType:
        """
        Uploads a JSON/CSV conversation dataset to /dataset/upload/conversations.

        Args:
            file_path: Path to the dataset file (.json or .csv).
            dataset_name: Dataset name to be saved on the platform.
            customer_message_column_name: Name of column with user messages.
            agent_reply_column_name: Name of column with assistant replies.

        Returns:
            UploadDatasetResponseType: ID of uploaded dataset and metadata.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        form_data = aiohttp.FormData()
        form_data.add_field('file', file_path.open('rb'), filename=file_path.name, content_type='application/json')
        form_data.add_field('dataset_name', dataset_name)
        form_data.add_field('space_id', self.space_id)
        form_data.add_field('customer_message_column_name', customer_message_column_name)
        form_data.add_field('agent_reply_column_name', agent_reply_column_name)

        resp = await self.send_form_request('/api/v1/dataset/upload/conversations', form_data, method="POST")

        return resp
