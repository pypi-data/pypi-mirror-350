from typing import Literal

import aiohttp
from aiohttp import FormData


class BaseService:
    def __init__(self, access_token: str, space_id: str) -> None:
        self.base_url = 'https://api.collinear.ai'
        self.space_id = space_id
        self.access_token = access_token

    def set_access_token(self, access_token: str):
        """
        Sets the access token for the entire SDK.
        """
        self.access_token = access_token
        return self

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_form_data_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    async def send_request(self, url: str, method: Literal["POST", "GET", "PUT", "DELETE", "PATCH"] = "GET",
                           data: dict = None) -> dict:
        full_url = f"{self.base_url}{url}"
        if data is not None:
            data = {
                "space_id": self.space_id,
                **data
            }

        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=method,
                    url=full_url,
                    headers=self.get_headers(),
                    json=data
            ) as response:
                try:
                    if response.status >= 400:
                        error_text = await response.text()
                        raise Exception(error_text)
                    else:
                        response_data = await response.json()
                        return response_data
                except aiohttp.ContentTypeError:
                    error_text = await response.text()
                    raise Exception(f"Response is not JSON: {error_text}")
                except aiohttp.ClientResponseError as e:
                    error_text = await response.text()  # Capture the response content for debugging
                    raise Exception(f"HTTP error occurred: {e.status} - {error_text}")
                except Exception as e:
                    raise Exception(f"Unexpected error: {str(e)}")

    async def send_form_request(self, url: str, form_data: FormData,
                                method: Literal["POST", "GET", "PUT", "DELETE", "PATCH"] = "GET",
                                ) -> dict:
        full_url = f"{self.base_url}{url}"
        if form_data is not None:
            form_data.add_field('space_id', self.space_id)

        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=method,
                    url=full_url,
                    headers=self.get_form_data_headers(),
                    data=form_data
            ) as response:
                try:
                    if response.status >= 400:
                        error_text = await response.text()
                        raise Exception(error_text)
                    file_name = None
                    disposition = response.headers.get('Content-Disposition', '')
                    if 'filename=' in disposition:
                        file_name:str = disposition.split('filename=')[1].strip('"')
                        file_name = file_name.replace('.json','')

                    file_content = await response.json()  # Read binary content
                    return {
                        "data_id": file_name,
                        "data": file_content
                    }
                except aiohttp.ContentTypeError:
                    error_text = await response.text()
                    raise Exception(f"Response is not JSON: {error_text}")
                except aiohttp.ClientResponseError as e:
                    error_text = await response.text()  # Capture the response content for debugging
                    raise Exception(f"HTTP error occurred: {e.status} - {error_text}")
                except Exception as e:
                    raise Exception(f"Unexpected error: {str(e)}")
