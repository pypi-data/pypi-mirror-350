import requests
from werkzeug.exceptions import Unauthorized


class Response():
    success: bool = False
    message: str = 'Something went wrong'

    def __init__(self, response):
        if response.status_code == requests.codes.ok:
            self.handle_response_ok(response)
        elif response.status_code == 400:
            self.handle_bad_request(response)
        elif response.status_code == 401:
            self.handle_unauthorized()
        elif response.status_code == 204:
            self.handle_no_content()

    def handle_response_ok(self, response):
        self.data = response.json()
        if not self.data.get('error', None):
            self.message = 'Success'
            self.success = True
        else:
            self.message = self.data['error']
            self.success = False

    def handle_bad_request(self, response):
        self.success = False
        self.message = response.json()

    def handle_not_found(self):
        self.success = False
        self.message = 'Not found'

    def handle_no_content(self):
        self.success = True
        self.message = 'Deleted'

    def handle_unauthorized(self):
        raise Unauthorized('Could not authenticate user in GetAccept')

    def serialize(self):
        return self.__dict__


class DocumentsResponse(Response):
    def handle_response_ok(self, response):
        data = response.json()
        self.success = True
        self.message = 'Success'
        self.documents = data


class TemplatesResponse(Response):
    def handle_response_ok(self, response):
        data = response.json()
        if not isinstance(data, dict):
            data = dict()
        self.success = True
        self.message = 'Success'
        self.templates = data.get('templates', [])


class TemplateFieldsResponse(Response):
    def handle_no_content(self):
        self.success = True
        self.message = 'Success'
        self.data = {'fields': []}
