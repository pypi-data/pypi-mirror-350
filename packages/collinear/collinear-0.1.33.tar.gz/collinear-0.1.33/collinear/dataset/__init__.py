import json
import uuid
from pathlib import Path
import aiohttp
import pandas as pd

from collinear.BaseService import BaseService
from collinear.dataset.types import UploadDatasetResponseType,CreateDatasetResponseType
from collinear.dataset.schema import CreateNewDatasetRequestDTO


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
        Uploads a JSON/CSV conversation dataset to Collinear Platform.

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
    
    async def create_dataset(self, request: CreateNewDatasetRequestDTO ) -> UploadDatasetResponseType:
        """
        Calls the /api/v1/dataset/ endpoint to create a new dataset directly via SDK.

        Args:
            dataset_name: Name of the dataset to create.
            conversations: A list of conversation dicts, where each dict has conv_prefix, response, ground_truth, judgements, etc.
            parent_dataset_id: Optional parent dataset UUID for versioning.

        Returns:
            UploadDatasetResponseType: ID and message from the backend.

        EXAMPLE PAYLOAD = 
        {
        "name": "sample_dataset_name",
        "space_id":"ac5b59fe-e9e6-404a-97de-972c2390948f",
        "parent_dataset_id":"add_if_available"
        [
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
        }
        """
        

        resp = await self.send_request(
            url="/api/v1/dataset/",
            method="POST",
            data=request
        )
        return CreateDatasetResponseType(dataset_id=resp["dataset_id"], message=resp["message"])
    
    
    async def download_dataset_json(self, dataset_id: str, save_path: str = None) -> bytes:
        """
        Downloads the dataset JSON for a given dataset ID.

        Args:
            dataset_id (str): The UUID of the dataset to download.
            save_path (str, optional): If provided, saves the file to disk.

        Returns:
            bytes: The raw byte content of the downloaded JSON file.
        """

        url = f"/api/v1/dataset/{dataset_id}/download"

        resp = await self.send_request(
            url=url,
            method="GET",
            return_bytes=True  # <-- Make sure your send_request can return raw bytes
        )

        if save_path:
            with open(save_path, "wb") as f:
                f.write(resp)

        return resp

    async def fetch_uploaded_datasets_by_space(self, page: int = 0, page_size: int = 10) -> dict:
        """
        Fetches a paginated list of uploaded datasets for the current space via GraphQL.

        Args:
            page (int): The page number to fetch.
            page_size (int): The number of datasets per page.

        Returns:
            dict: Parsed response from GraphQL containing datasets and count.
        """

        graphql_url = f"/graphql"

        query = """
        query getUploadedDatasetBySpaceIdAndPage($spaceId:UUID!,$page:Int!,$pageSize:Int!){
            getUploadedDatasetByPageAndSpaceId(spaceId:$spaceId,page:$page,limit:$pageSize) {
                count
                datasets {
                id
                name
                rows
                createdBy
                createdAt
                }
            }
        }
        """

        payload = {
            "operationName": "getUploadedDatasetBySpaceIdAndPage",
            "variables": {
                "spaceId": self.space_id,
                "page": page,
                "pageSize": page_size
            },
            "query": query
        }

        resp = await self.send_request(
            url=graphql_url,
            method="POST",
            data=payload
        )
        if 'errors' in resp:
            raise Exception(f"GraphQL errors: {json.dumps(resp['errors'], indent=2)}")

        if 'data' not in resp or resp['data']['getUploadedDatasetByPageAndSpaceId'] is None:
            raise Exception(f"GraphQL response missing 'data': {json.dumps(resp, indent=2)}")

        return resp['data']['getUploadedDatasetByPageAndSpaceId']
    

    async def fetch_dataset_rows_by_id(self, dataset_id: str, page: int = 0, page_size: int = 10) -> dict:
        """
        Fetches dataset rows for a given dataset ID using GraphQL.

        Args:
            dataset_id (str): UUID of the dataset.
            page (int): Page number to fetch.
            page_size (int): Number of rows per page.

        Returns:
            dict: Parsed GraphQL response with dataset rows and count.
        """

        graphql_url = f"/graphql"

        query = """
        query getDatasetRowsByDatasetId($datasetId: UUID!, $page: Int!, $pageSize: Int!) {
          getDatasetRowsByDatasetId(
            datasetId: $datasetId
            page: $page
            pageSize: $pageSize
          ) {
            count
            rows {
              id
              convPrefix {
                role
                content
              }
              response {
                role
                content
              }
              groundTruth
              context
            }
          }
        }
        """

        payload = {
            "operationName": "getDatasetRowsByDatasetId",
            "variables": {
                "datasetId": dataset_id,
                "page": page,
                "pageSize": page_size
            },
            "query": query
        }

        resp = await self.send_request(
            url=graphql_url,
            method="POST",
            data=payload
        )

        if 'errors' in resp:
            raise Exception(f"GraphQL errors: {json.dumps(resp['errors'], indent=2)}")

        if 'data' not in resp or resp['data']['getDatasetRowsByDatasetId'] is None:
            raise Exception(f"GraphQL response missing 'data': {json.dumps(resp, indent=2)}")

        return resp['data']['getDatasetRowsByDatasetId']

