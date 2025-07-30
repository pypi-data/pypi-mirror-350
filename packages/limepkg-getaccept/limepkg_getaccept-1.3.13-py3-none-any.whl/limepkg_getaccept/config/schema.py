from marshmallow import Schema, fields
from lime_type.fields import LimeTypeField, LimePropertyField


def create_schema(application):
    class CompanySchema(Schema):
        class Meta:
            ordered = True

        limetype = LimeTypeField(
            application=application,
            metadata=dict(
                title="Company limetype",
                description="Choose limetype which represents a company",
            ),
        )

    class DealSchema(Schema):
        class Meta:
            ordered = True

        limetype = LimeTypeField(
            application=application,
            metadata=dict(
                title="Deal limetype",
                description="Choose limetype which represents a deal",
            ),
        )

        deal_value = LimePropertyField(
            application=application,
            limetype_field="limetype",
            metadata=dict(
                title="Deal value property",
                description="Limetype property which represents deal value",
            ),
        )

        personFields = fields.List(
            LimePropertyField(
                application=application,
                metadata=dict(
                    title="Person/s relation property ",
                    description="Limetype property which represents relation to person",
                ),
            ),
            title="List of deal properties for related persons",
        )

    class DealSettingSchema(Schema):
        class Meta:
            ordered = True

        get_persons_from_related_company = fields.Boolean(
            title="Auto insert persons from related company",
            description="Enable/disable Auto insert persons from related company",
        )

        dealSettings = fields.List(
            fields.Nested(DealSchema), title="Custom deal object config"
        )

    class PersonSchema(Schema):
        class Meta:
            ordered = True

        limetype = LimeTypeField(
            application=application,
            metadata=dict(
                title="Person limetype",
                description="Choose limetype which represents a person",
            ),
        )

        use_for_search = fields.Boolean(
            title="Use this limetype for search",
            description="Enable/disable this limetype available for search",
        )

        first_name = LimePropertyField(
            application=application,
            limetype_field="limetype",
            metadata=dict(
                title="First name",
                description="Limetype property which represents first name",
            ),
        )
        last_name = LimePropertyField(
            application=application,
            limetype_field="limetype",
            metadata=dict(
                title="Last name",
                description="Limetype property which represents last name",
            ),
        )
        email = LimePropertyField(
            application=application,
            limetype_field="limetype",
            metadata=dict(
                title="Email",
                description="Limetype property which represents email",
            ),
        )
        mobile = LimePropertyField(
            application=application,
            limetype_field="limetype",
            metadata=dict(
                title="Mobile phone",
                description="Limetype property which represents phone",
            ),
        )
        company = LimePropertyField(
            application=application,
            limetype_field="limetype",
            metadata=dict(
                title="Company",
                description="Limetype property which represents company",
            ),
        )
        company_name = LimePropertyField(
            application=application,
            limetype_field="company",
            metadata=dict(
                title="Company name",
                description="Limetype property which represents company",
            ),
        )

    class PersonSettingsSchema(Schema):
        class Meta:
            ordered = True

        personSettings = fields.List(
            fields.Nested(PersonSchema), title="Person properties"
        )

    class CoworkerSchema(Schema):
        class Meta:
            ordered = True

        limetype = LimeTypeField(
            application=application,
            metadata=dict(
                title="Coworker limetype",
                description="Choose limetype which represents a user",
            ),
        )
        first_name = LimePropertyField(
            application=application,
            limetype_field="limetype",
            title="First name",
            description="Limetype property which represents first name",
        )
        last_name = LimePropertyField(
            application=application,
            limetype_field="limetype",
            title="Last name",
            description="Limetype property which represents last name",
        )
        email = LimePropertyField(
            application=application,
            limetype_field="limetype",
            title="Email",
            description="Limetype property which represents email",
        )
        mobile = LimePropertyField(
            application=application,
            limetype_field="limetype",
            title="Mobile phone",
            description="Limetype property which represents phone",
        )

        class Meta:
            ordered = True

    class GetacceptEsigningConfigSchema(Schema):
        class Meta:
            ordered = True

        use_custom_config = fields.Boolean(
            title="Use custom config",
            description="Enable/disable usage of the custom config for custom limetypes",
        )

        use_default_persons_object = fields.Boolean(
            title="Use default persons object",
            description="Enable/disable usage of the default persons object for contacts searching",
        )
        company = fields.Nested(title="Company", nested=CompanySchema)
        deal = fields.Nested(title="Deals settings", nested=DealSettingSchema)
        person = fields.Nested(title="Persons settings", nested=PersonSettingsSchema)
        coworker = fields.Nested(title="Coworker", nested=CoworkerSchema)

    return GetacceptEsigningConfigSchema()
