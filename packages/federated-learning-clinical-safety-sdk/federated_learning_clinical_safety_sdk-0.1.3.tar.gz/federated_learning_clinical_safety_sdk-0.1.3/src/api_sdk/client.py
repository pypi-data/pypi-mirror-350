# src/my_api_sdk/client.py
import requests
from .models import FlModel, LocalModel
from .exceptions import APIError

class APIClient:
    def __init__(self, base_url: str, token: str):
        self.base = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Token {token}'})

    def list_models(self) -> list[FlModel]:
        url = f"{self.base}/models/"
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise APIError.from_response(resp)
        return [FlModel(**item) for item in resp.json()]

    def get_model(self, model_id: int) -> FlModel:
        url = f"{self.base}/models/{model_id}/"
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise APIError.from_response(resp)
        return FlModel(**resp.json())

    def create_model(self, model: FlModel) -> FlModel:
        url = f"{self.base}/models/"
        payload = model.dict(exclude_unset=True)
        resp = self.session.post(url, json=payload)
        if resp.status_code != 201:
            raise APIError.from_response(resp)
        return FlModel(**resp.json())

    def list_local_models(self, model_id: int) -> list[LocalModel]:
        url = f"{self.base}/models/{model_id}/locals/"
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise APIError.from_response(resp)
        return [LocalModel(**item) for item in resp.json()]

    # you can add update_model, delete_model, create_local_model, etc.
