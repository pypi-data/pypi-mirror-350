from collinear import Collinear
import pandas as pd
import asyncio
import uuid
space_id = "47d50fad-1903-4fba-841e-119405fbc444"
collinear=Collinear(access_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBPTXVVV1AxT1N5Yy1QQ0VjaWcxLSJ9.eyJpc3MiOiJodHRwczovL2NvbGxpbmVhci1haS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwNDA0NDA3NDE0MDY5Nzg0MTYiLCJhdWQiOlsiaHR0cHM6Ly9jb2xsaW5lYXItYWkudXMuYXV0aDAuY29tL2FwaS92Mi8iLCJodHRwczovL2NvbGxpbmVhci1haS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzQ3MTQ3NTE5LCJleHAiOjE3NDcyMzM5MTksInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MiLCJhenAiOiJpMWVHV1lmNDJlR3lUUHREakhreEZscUJCMENBWFFJMiJ9.LCyWdwUxT4GUSm42sKZ4Tjrq-pKVMKwYGkCeZsmxQvf-kH8pauzNhtHVexlWcJHnOQ9RXL9Y3tKry6fcXGpGuoR3AJBEkTOgNniFK0Ft9Iww9gKjrV38NRcXTqx6g45pFVC3XpW6Hrqd32woB1Kk0GIXFj1bOQJwkk1nTkQjLeZIwE0Dzhmb0J08nXduJ6bN9Zg-PYbvSOjNfbwswNe6Uc_DQ4TOrRvmTLI-wgXXV0ytdFw0ahme-qRSYeEbs5XG_GdAnMHxriDkHX_se1mgdamFBMVYfMQax_9rKtnfdcifridal8YNvq0bVRL9UImPTCRiRfaVL-3E04djJeDUDQ', space_id="dc5b59fe-f9e6-404a-97df-972c2390948e")
data = {
    "conversation_prefix":[{
        "role":"user",
        "content":"How do actinomycetes differ from other types of bacteria in terms of their structure?"
    }],
    "response":{
        "role":"assistant",
        "content":"Actinomycetes differ from other bacteria in that they form filamentous chains of single cells, which is a unique characteristic among prokaryotes."
        }
    }
# Extract fields
user_msg = data["conversation_prefix"]
assistant_msg = data["response"]
# Convert to DataFrame
df = pd.DataFrame([{
    "conversation_prefix": user_msg,
    "response": assistant_msg
}])
# print(df)
judge_ids=["eaf9f29c-b6ec-4613-898f-26ad83c2d2a3","02c293b3-9e58-4dab-b887-3bfafbf47572"]
async def run_judge():
    collinear_model_judged = await collinear.judge.run_judges_on_dataset(
        data=df,
        conv_prefix_column_name="conversation_prefix",
        response_column_name="response",
        space_id=space_id,
        judge_ids=judge_ids
        )
#     collinear_model_judged = await collinear.judge.run_judge_on_dataset(data=df,conv_prefix_column_name="conversation_prefix",response_column_name="response",space_id=space_id,judge_id="6a403e9a-32d7-485a-bea6-8e3a7c18a5fa")
    print(collinear_model_judged)
# async def run_judge():
#     collinear_model_judged = await collinear.judge.run_judge_on_dataset(
#         data=df,
#         conv_prefix_column_name="conversation_prefix",
#         response_column_name="response",
#         space_id=space_id,
#         judge_id="db6417a2-5820-4363-99fb-0269603daaeb",
#         judge_name="veritas"
#     )
#     print(collinear_model_judged)
#     return collinear_model_judged

# Config
ACCESS_TOKEN = "64529d27-08c7-46fc-ba2e-3aa216ac79b4"
SPACE_ID = "47d50fad-1903-4fba-841e-119405fbc444"
FILE_PATH = "conversations_3_masked.json"
DATASET_NAME = "sdk_test_conversation_dataset_"+str(uuid.uuid4())
EVALUATION_NAME = "sdk_test_conversation_assessment_"+str(uuid.uuid4())
JUDGE_IDS = [
    "5e9e1ce1-f5f9-467f-8a54-ccaf0a324b0a",
    "89d8206f-ba0b-4bfc-9d77-31506695433d"
]
CUSTOMER_COL = "customer_message"
AGENT_COL = "agent_reply"
collinear=Collinear(access_token=ACCESS_TOKEN, space_id=SPACE_ID)

async def upload_and_assess():
    try:
        # Upload dataset
        print("📤 Uploading dataset...")
        upload_result = await collinear.dataset.upload_conversation_dataset(
            file_path=FILE_PATH,
            dataset_name=DATASET_NAME,
            customer_message_column_name=CUSTOMER_COL,
            agent_reply_column_name=AGENT_COL
        )
        print("Full upload result:", upload_result)
        
        # Try to get dataset_id from the response
        if isinstance(upload_result, dict):
            if "data" in upload_result and "data" in upload_result["data"] and "dataset_id" in upload_result["data"]["data"]:
                dataset_id = upload_result["data"]["data"]["dataset_id"]
            elif "data" in upload_result and "dataset_id" in upload_result["data"]:
                dataset_id = upload_result["data"]["dataset_id"]
            else:
                raise KeyError("Could not find dataset_id in the response. Response structure: " + str(upload_result))
        else:
            raise TypeError(f"Expected dict response, got {type(upload_result)}")
        
        print(f"✅ Dataset uploaded. Dataset ID: {dataset_id}")

        # Run assessment
        print("🚀 Running assessment...")
        try:
            run_result = await collinear.evaluation.run_assessment(
                dataset_id=dataset_id,
                name=EVALUATION_NAME,
                judge_ids=JUDGE_IDS
            )
            print("✅ Assessment run started.")
            print(run_result)
        except Exception as e:
            print(f"❌ Error running assessment: {str(e)}")
            print("Full error details:", e)
            
    except Exception as e:
        print(f"❌ Error in upload_and_assess: {str(e)}")
        print("Full error details:", e)

# Run the async flow
if __name__ == "__main__":
    asyncio.run(upload_and_assess())

# if __name__ == "__main__":
#     rspose = asyncio.run(run_judge())