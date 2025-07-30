import requests
import os
from .types import (
    Response,
    DocumentsResponse,
    TemplatesResponse,
    TemplateFieldsResponse,
)
from .lime_helpers import match_merge_fields
import logging
import bugsnag
import base64

logger = logging.getLogger(__name__)


class GetAccept:
    def __init__(self):
        self.requests = requests.Session()
        self.requests.headers = {"Content-type", "application/json"}

    def create_document(self, params, token: str) -> Response:
        endpoint = get_endpoint("documents")
        response = self.post_request(endpoint, params, token)
        return Response(response).serialize()

    def update_document(self, params, token: str) -> Response:
        endpoint = get_endpoint("documents/{}".format(params["document_id"]))
        response = self.put_request(
            endpoint, {"external_client_id": "Lime CRM Web"}, token
        )
        logger.info("---------------")
        logger.info(response)
        return Response(response).serialize()

    def seal_document(self, document_id: str, token: str) -> Response:
        endpoint = get_endpoint("documents/{}/seal".format(document_id))
        response = self.post_request(endpoint, None, token)
        return Response(response).serialize()

    def send_document(self, document_id: str, token: str) -> Response:
        endpoint = get_endpoint("documents/{}/send".format(document_id))
        response = self.post_request(endpoint, None, token)
        return Response(response).serialize()

    def fetch_templates(self, params, token: str) -> TemplatesResponse:
        endpoint = get_endpoint("templates?showall=true")
        response = self.get_request(endpoint, params, token)
        return TemplatesResponse(response).serialize()

    def fetch_template_fields(
        self, limeobject, template_id: str, token: str
    ) -> TemplateFieldsResponse:
        endpoint = get_endpoint("templates/{}/fields".format(template_id))
        response = self.get_request(endpoint, None, token)

        response_obj = TemplateFieldsResponse(response)
        response_obj.data["fields"] = match_merge_fields(limeobject, response_obj.data)
        return response_obj.serialize()

    def fetch_template_roles(self, template_id: str, token: str) -> Response:
        endpoint = get_endpoint("templates/{}/roles".format(template_id))
        response = self.get_request(endpoint, None, token)
        return Response(response).serialize()

    def fetch_me(self, token: str) -> Response:
        endpoint = get_endpoint("users/me")
        response = self.get_request(endpoint, None, token)
        return Response(response).serialize()

    def fetch_sent_documents(self, params, token):
        endpoint = get_endpoint("documents")
        response = self.get_request(endpoint, params, token)
        return DocumentsResponse(response).serialize()

    def fetch_document_detail(self, document_id: str, token: str) -> Response:
        endpoint = get_endpoint(
            "documents/{}?with_pages=true&with_stats=true".format(document_id)
        )
        response = self.get_request(endpoint, None, token)
        return Response(response).serialize()

    def delete_document(self, document_id: str, token):
        endpoint = get_endpoint("documents/{}".format(document_id))
        response = self.delete_request(endpoint, token)
        return Response(response).serialize()

    def upload_file(self, file_name, file_data, token):
        endpoint = get_endpoint("upload")

        file_content = base64.b64encode(file_data.getvalue()).decode()
        response = self.post_request(
            endpoint, {"file_name": file_name, "file_content": file_content}, token
        )
        return Response(response).serialize()

    def login(self, email: str, password: str) -> Response:
        endpoint = get_endpoint("auth")
        data = {"email": email, "password": password, "client_id": "Lime Web CRM"}
        response = self.requests.post(endpoint, json=data)
        return Response(response).serialize()

    def signup(
        self,
        email: str,
        mobile: str,
        password: str,
        first_name: str,
        last_name: str,
        country_code: str,
        company: str,
    ):
        endpoint = get_endpoint("register")
        payload = {
            "user_registration_source": "Lime CRM Web",
            "client_id": "Lime CRM Web",
            "auto_login": True,
            "skip_invitation": True,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": "{0} {1}".format(first_name, last_name),
            "mobile": mobile,
            "entity_country_code": country_code,
            "entity_name": company,
        }
        response = self.requests.post(endpoint, json=payload)
        return Response(response).serialize()

    def refresh_token(self, entity_id, token) -> Response:
        action = "refresh/{}".format(entity_id) if entity_id else "refresh"
        endpoint = get_endpoint(action)

        response = self.get_request(endpoint, None, token)
        return Response(response).serialize()

    def test_token(self, access_token, expires_in: int):
        endpoint = get_endpoint("test")
        response = self.get_request(endpoint, None, access_token)
        max_remaining_expiration_seconds = 7 * 3600 * 24

        if response.status_code != requests.codes.ok:
            return Response(response).serialize()

        if expires_in < max_remaining_expiration_seconds:
            return self.refresh_token("", access_token)

        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "expires_in": expires_in,
            },
        }

    def get_request(self, url: str, params, token: str):
        headers = {"Authorization": "Bearer {}".format(token)}
        response = self.requests.get(url, headers=headers, params=params)
        return response

    def post_request(self, url: str, data, token: str):
        headers = {"Authorization": "Bearer {}".format(token)}
        response = self.requests.post(url, json=data, headers=headers)
        return response

    def put_request(self, url: str, data, token: str):
        headers = {"Authorization": "Bearer {}".format(token)}
        response = self.requests.put(url, json=data, headers=headers)
        return response

    def delete_request(self, url: str, token: str):
        headers = {"Authorization": "Bearer {}".format(token)}
        response = self.requests.delete(url, headers=headers)
        return response

    def entity(self, token: str) -> Response:
        endpoint = get_endpoint("entity")
        response = self.get_request(endpoint, None, token)
        return Response(response).serialize()

    def videos(self, token: str) -> Response:
        endpoint = get_endpoint("videos")
        response = self.get_request(endpoint, None, token)
        return Response(response).serialize()


def get_endpoint(path: str):
    url = os.environ.get("GA_URL", "https://api.getaccept.com/v1/")
    return "{}{}".format(url, path)
