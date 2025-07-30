import uuid
import asyncio
from collinear.BaseService import BaseService
from collections import defaultdict



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

    async def run_assessment(
        self,
        dataset_id: str,
        name: str,
        judge_ids: list[uuid.UUID],
        roll_data: bool = True,
        batch_size: int = 3
    ) -> dict:
        """
        Triggers a multi-judge assessment on uploaded dataset with batched processing.
        
        Args:
            dataset_id: ID of the dataset uploaded for evaluation
            name: Name of this evaluation run
            judge_ids: List of judge IDs to evaluate with
            roll_data: Whether to roll up conversation data
            batch_size: Maximum number of judges per API call (default: 3)
        
        Returns:
            Aggregated response from all batches in format:
            {
                "results": [list_of_all_responses],
                "aggregated_scores": {judge_id: average_score},
                "success_count": int,
                "failed_batches": list
            }
        """
        if not judge_ids:
            raise ValueError("At least one judge ID must be provided")

        all_results = []
        failed_batches = []
        aggregated_scores = defaultdict(list)

        # Process judges in batches
        for i in range(0, len(judge_ids), batch_size):
            batch = judge_ids[i:i + batch_size]
            try:
                payload = {
                    "dataset_id": dataset_id,
                    "space_id": self.space_id,
                    "name": f"{name}_batch_{i//batch_size + 1}",
                    "judge_ids": batch,
                    "roll_data": roll_data
                }
                
                response = await self.send_request(
                    '/api/v1/dataset/assess/run',
                    "POST",
                    payload
                )
                all_results.append(response['data'])
            except Exception as e:
                failed_batches.append({
                    "batch": batch,
                    "error": str(e)
                })
                continue
        return all_results  # or response['data']['run_id'] if specific ID is returned
