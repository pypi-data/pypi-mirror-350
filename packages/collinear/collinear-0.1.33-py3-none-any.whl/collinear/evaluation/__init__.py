import uuid
import asyncio
from collinear.BaseService import BaseService


class Evaluation(BaseService):
    def __init__(self, access_token: str, space_id: str) -> None:
        super().__init__(access_token, space_id)

    async def run_evaluation(self, uploaded_dataset_id: uuid.UUID, judge_id: uuid.UUID, name: str):
        """
        Trigger Evaluation from sdk
        Args:
            name: Name of the evaluation.
            uploaded_dataset_id: ID of the uploaded dataset.
            judge_id: ID of the judge.

        Returns:
            UploadDatasetResponseType: ID of the uploaded dataset and rows.
        """

        data = await self.send_request('/api/v1/evaluation', "POST",{
            "dataset_id": str(uploaded_dataset_id),
            "judge_id": str(judge_id),
            "name": name
        })
        return data['data']['eval_id']

    async def run_assessment(self, dataset_id: str, name: str, judge_ids: list[uuid.UUID]) -> str:
        """
        Triggers a multi-judge assessment on uploaded dataset.

        Args:
            dataset_id: ID of the dataset uploaded for evaluation.
            name: Name of this evaluation run.
            judge_ids: List of judge IDs to evaluate with.

        Returns:
            Evaluation run ID or full metadata (based on API response).
        """
        payload = {
            "dataset_id": dataset_id,
            "space_id": self.space_id,
            "name": name,
            "judge_ids": judge_ids
        }

        response = await self.send_request('/api/v1/dataset/assess/run', "POST", payload)
        return response['data']  # or response['data']['run_id'] if specific ID is returned
