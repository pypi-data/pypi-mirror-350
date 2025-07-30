import webargs.fields as fields
from marshmallow import (Schema, validates_schema,
                         ValidationError, validate, EXCLUDE)
from webargs.flaskparser import FlaskParser

import logging

logger = logging.getLogger(__name__)

VALID_COUNTRY_CODES = (
    'SE',
    'DK',
    'FI',
    'NO',
    'GB',
    'US',
    'OT',
)


class SimpleSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class SchemaWithLimeObject(SimpleSchema):
    limetype = fields.String(required=True)
    record_id = fields.Integer(required=True)

    @validates_schema
    def event_must_exist(self, data, **kwargs):
        """Validates that the event (limetype + event name) exists"""
        if not data:
            raise ValidationError("No data supplied to endpoint")
        app = self.context.get('application')
        if data['limetype'] in available_limetypes(app):
            return True
        raise ValidationError('No such limetype')


class AuthSchema(SimpleSchema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class SignupSchema(AuthSchema):
    company = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    country_code = fields.String(
        required=True, validate=validate.OneOf(VALID_COUNTRY_CODES))
    mobile = fields.String(required=False)


class RefreshTokenSchema(SimpleSchema):
    access_token = fields.String(required=True)
    expires_in = fields.Integer(required=True)


class TemplatesSchema(SimpleSchema):
    folder_id = fields.String(required=False)


class TemplateSchema(SchemaWithLimeObject):
    template_id = fields.String(required=True)


class SwitchEntitySchema(SimpleSchema):
    entity_id = fields.String(required=True)


class SearchPersonSchema(SimpleSchema):
    search = fields.String(required=True)
    limit = fields.Integer(default=10)
    offset = fields.Integer(default=0)


class SentDocumentsSchema(SimpleSchema):
    external_id = fields.String(required=True)


class GADocumentSchema(SimpleSchema):
    document_id = fields.String(required=False)


class LimeDocumentSchema(SimpleSchema):
    document_id = fields.Integer(required=False)
    file = fields.Raw(type='file', required=False)


class SenderSchema(SimpleSchema):
    email = fields.String(required=True)
    name = fields.String(required=True)
    sender_id = fields.String(required=True)
    thumb_url = fields.String(required=False)


class RecipientSchema(SimpleSchema):
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    fullname = fields.String(required=True)
    email = fields.String(required=False)
    mobile = fields.String(required=False)
    role = fields.String(required=True)
    role_id = fields.String(required=False)


class CustomFieldSchema(SimpleSchema):
    id = fields.String(required=True)
    value = fields.String(required=True)


class CreateDocumentSchema(SimpleSchema):
    is_automatic_sending = fields.Boolean(required=True)
    is_signing = fields.Boolean(required=True)
    is_signing_order = fields.Boolean(required=False, default=False)
    is_selfsign = fields.Boolean(required=False, default=False)
    document_type = fields.String(required=False, default='sales')
    external_id = fields.String(required=True)
    is_video = fields.Boolean(required=False, default=False)
    video_id = fields.String(required=False, default=None)
    value = fields.Integer(required=False, default=0)
    name = fields.String(required=True)
    recipients = fields.Nested(RecipientSchema, many=True)
    sign_date = fields.String(required=False)
    contract_start_date = fields.String(required=False)
    contract_end_date = fields.String(required=False)
    template_id = fields.String(required=False)
    custom_fields = fields.Nested(CustomFieldSchema, required=False, many=True)
    file_ids = fields.String(required=False)
    email_send_subject = fields.String(required=True)
    email_send_message = fields.String(required=True)
    is_sms_sending = fields.Boolean(required=True, default=False)


class UploadDocumentScheme(SimpleSchema):
    external_client_id = fields.String(required=False)
    document_id = fields.String(required=False)


def available_limetypes(application):
    return [limetype.name for limetype in application.limetypes.get_all()]


def validate_args(request, args, schema):
    try:
        return schema.load(args)
    except Exception as e:
        FlaskParser().handle_error(e, request, schema, None, None)
