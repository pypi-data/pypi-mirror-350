from lime_filter import Filter, OrOperator, EqualsOperator
from lime_filter.filter import LikeOperator
import datetime
import bugsnag
from lime_type.limeobjects import (
    BelongsToPropertyAccessor,
    OptionPropertyAccessor,
    SetPropertyAccessor,
    HasManyPropertyAccessor,
)
from lime_application import get_application, list_applications
import json
import traceback

from limepkg_getaccept.config import RuntimeConfig


def _serialize_properties_and_values(items):
    def serialize_item(item):
        if isinstance(item, datetime.datetime) or isinstance(item, datetime.date):
            return item.strftime("%Y-%m-%d")
        return item

    return_dict = {}
    for k, i in items.items():
        return_dict[k] = serialize_item(i)
    return return_dict


def removeDuplicates(items):
    if len(items) > 0:
        newlist = [items[0]]
        for e in items:
            if e not in newlist:
                newlist.append(e)
        return newlist

    return []


def get_filter(limetype_config, value):
    filter = None
    for key, field in limetype_config.items():
        if key == "limetype":
            continue
        operator = LikeOperator(field, value)
        if not filter:
            filter = operator
            continue
        filter = OrOperator(operator, filter)
    return Filter(filter)


def search_lime_objects(app, contact_type, search, limit, offset):
    limetype_config = get_plugin_config(app)[contact_type]
    contacts = []
    try:
        if contact_type == "person":
            if limetype_config.get("personSettings"):
                personSettings = limetype_config.get("personSettings")
                for prop in personSettings:
                    if prop.get("use_for_search"):
                        limeobject = app.limetypes.get_limetype(prop["limetype"])
                        prop.pop("use_for_search")
                        if "company_name" in prop:
                            prop.pop("company_name")
                        filter = get_filter(prop, search)
                        contacts.extend(
                            [
                                _serialize_properties_and_values(
                                    get_limetype_fields(obj, app)
                                )
                                for obj in limeobject.get_all(
                                    filter=filter, limit=limit, offset=offset
                                )
                            ]
                        )
        if contact_type == "coworker":
            limetype_config = get_plugin_config(app)[contact_type]
            limeobject = app.limetypes.get_limetype(limetype_config["limetype"])
            if "company_name" in limetype_config:
                prop.pop("company_name")
            filter = get_filter(limetype_config, search)
            contacts.extend(
                [
                    _serialize_properties_and_values(get_limetype_fields(obj, app))
                    for obj in limeobject.get_all(
                        filter=filter, limit=limit, offset=offset
                    )
                ]
            )
    except Exception as e:
        traceback.print_exc()
        print(e)

    return contacts


def search_lime_persons(app, search, limit, offset):
    limetype_config = {
        "limetype": "person",
        "first_name": "firstname",
        "last_name": "lastname",
        "email": "email",
        "mobile": "mobilephone",
        "company": "company",
    }
    use_default_persons_object = get_plugin_config(app).get(
        "use_default_persons_object"
    )
    if use_default_persons_object:
        limetype = app.limetypes.get_limetype("person")
        filter = get_filter(limetype_config, search)
        return [
            _serialize_properties_and_values(
                get_limetype_fields(obj, app, limetype_config)
            )
            for obj in limetype.get_all(filter=filter, limit=limit, offset=offset)
        ]
    else:
        return []


def get_documents(app, limetype, record_id):
    documents = app.limetypes.get_limetype("document").get_all(
        filter=Filter(EqualsOperator(limetype, record_id))
    )
    documents_with_files = []
    supported_file_types = [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/pdf",
        "application/msword",
    ]
    for doc in documents:
        file = get_file_data(app, doc.id)
        if file != None:
            if file.mimetype in supported_file_types:
                documents_with_files.append(doc)

    return [dict(**doc.values(), id=doc.id) for doc in documents_with_files]


def get_contacts_for_current_limetype(app, limetype, record_id):
    config = get_plugin_config(app)
    contacts = []
    current_limetype = app.limetypes.get_limetype(limetype).get(record_id)
    properties = current_limetype.properties
    listOfExistingProperties = None

    dealSettingsForCurrentLimetype = next(
        (
            dealConfig
            for dealConfig in config["deal"]["dealSettings"]
            if dealConfig["limetype"] == limetype
        ),
        None,
    )

    if dealSettingsForCurrentLimetype:
        listOfExistingProperties = [
            setting
            for setting in dealSettingsForCurrentLimetype["personFields"]
            if hasattr(properties, setting)
        ]

    if limetype == config["company"]["limetype"]:
        try:
            contacts = list(
                app.limetypes.get_limetype("person").get_all(
                    filter=Filter(EqualsOperator(limetype, record_id))
                )
            )
        except Exception as e:
            print(e)
    if listOfExistingProperties:
        for exitingProperty in listOfExistingProperties:
            attributeByKey = getattr(properties, exitingProperty)
            if isinstance(attributeByKey, BelongsToPropertyAccessor):
                limeObject = attributeByKey.fetch()
                contacts.append(limeObject)

            if isinstance(attributeByKey, HasManyPropertyAccessor):
                limeObjects = attributeByKey.fetch()
                if limeObjects:
                    for limeObject in limeObjects:
                        contacts.append(limeObject)
    if (
        limetype != config["company"]["limetype"]
        and config["deal"]
        and config["deal"].get("get_persons_from_related_company")
    ):
        has_company = hasattr(properties, config["company"]["limetype"])
        related_company = (
            getattr(properties, config["company"]["limetype"]) if has_company else None
        )
        companyContacts = []
        personLimetypes = [
            personLimetype["limetype"]
            for personLimetype in config["person"]["personSettings"]
            if hasattr(properties, personLimetype["limetype"])
        ]
        for personLimetype in personLimetypes:
            try:
                result = app.limetypes.get_limetype(personLimetype).get_all(
                    filter=Filter(
                        EqualsOperator(
                            config["company"]["limetype"],
                            getattr(related_company, "id", None),
                        )
                    )
                )
                companyContacts.extend([i for i in result])
            except Exception as error:
                traceback.print_exc()
                print(error)
                bugsnag.notify(error)
        contacts.extend(companyContacts)
    if config.get("person") and config["person"]["personSettings"]:
        personLimetypes = [
            personLimetype["limetype"]
            for personLimetype in config["person"]["personSettings"]
        ]

        if limetype in personLimetypes:
            contacts.append(current_limetype)
    contacts = [get_limetype_fields(contact, app) for contact in contacts]
    return [
        _serialize_properties_and_values(contact)
        for contact in removeDuplicates(contacts)
    ]


def match_merge_fields(limeobject, data):
    fields = data.get("fields", [])
    for field in fields:
        value = get_merge_field_value(limeobject, field)
        field.update(
            {
                "field_label": field.get("field_label") or field.get("field_value"),
                "field_value": value,
            }
        )
    return fields


def get_file_data(app, document_id):
    document = app.limetypes.get_limetype("document").get(document_id)
    return document.properties.document.fetch()


def get_merge_field_value(limeobject, field):
    try:
        key = field["field_value"].replace("{{", "").replace("}}", "")

        value = _serialize_properties_and_values(get_lime_values(limeobject))[key]
        return value
    except Exception:
        return field["field_value"]


def extract_value(prop, fetch_nested=True):
    if isinstance(prop, BelongsToPropertyAccessor):
        nested_obj = prop.fetch()
        if not nested_obj or not fetch_nested:
            return prop.descriptive
        return {
            nested_prop.name: extract_value(nested_prop, False)
            for nested_prop in nested_obj.get_properties_with_value()
        }
    if isinstance(prop, OptionPropertyAccessor):
        return prop.value.key
    if isinstance(prop, SetPropertyAccessor):
        return [p.key for p in prop.value]
    if isinstance(prop, HasManyPropertyAccessor):
        if not fetch_nested:
            return prop.value
        result = []
        for nested_obj in prop.fetch():
            properties_dict = {
                nested_prop.name: extract_value(nested_prop, False)
                for nested_prop in nested_obj.get_properties_with_value()
            }
            result.append(properties_dict)
        return result
    return prop.value


def get_lime_values(limeobject):
    props = limeobject.properties

    def get_prop_names_to_ignore():
        ignored_props = {"*": ["history", "todo"]}
        return ignored_props.get(limeobject.limetype.name, ignored_props.get("*", []))

    values = {}

    for prop in props:
        if prop.name in get_prop_names_to_ignore():
            continue
        value = extract_value(prop)

        if isinstance(value, dict):
            for k, v in value.items():
                values[f"{prop.name}.{k}"] = v
        elif isinstance(value, list):
            for i, item in enumerate(value, 1):
                if isinstance(item, str):
                    values[f"{prop.name}.{i}"] = item
                else:
                    for k, v in item.items():
                        values[f"{prop.name}{i}.{k}"] = v
        elif isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
            values[f"{limeobject.limetype.name}.{prop.name}"] = value.strftime(
                "%Y-%m-%d"
            )
        else:
            values[f"{limeobject.limetype.name}.{prop.name}"] = value

    return values


def get_deal_value(limetype, limetype_id, app):
    config = get_plugin_config(app)
    limeobject = app.limetypes.get_limetype(limetype).get(limetype_id)
    properties = limeobject.properties

    dealSettingsForCurrentLimetype = next(
        (
            dealConfig
            for dealConfig in config["deal"]["dealSettings"]
            if dealConfig["limetype"] == limetype
        ),
        None,
    )
    if limeobject and dealSettingsForCurrentLimetype:
        if dealSettingsForCurrentLimetype.get("deal_value"):
            if hasattr(properties, dealSettingsForCurrentLimetype.get("deal_value")):
                return extract_value(
                    properties.__getattr__(
                        dealSettingsForCurrentLimetype.get("deal_value")
                    )
                )

    return "0"


def get_limetype_fields(obj, app, config=None):
    fields = {}
    props = obj.properties
    default_key = "company"
    for key, object in get_plugin_config(app).items():
        if not isinstance(object, dict):
            continue
        if object.get("limetype") == obj.limetype.name:
            default_key = key
            break
        if object.get("personSettings"):
            personSettings = next(
                (
                    prop
                    for prop in object.get("personSettings")
                    if prop.get("limetype") == obj.limetype.name
                ),
                None,
            )
            if personSettings:
                config = personSettings
    if not config:
        config = get_plugin_config(app)[default_key]

    for key, object_key in config.items():
        if key in ["company", "company_name"]:
            continue
        related_property = next(
            (prop for prop in props if prop.name == object_key), None
        )
        if not related_property:
            continue
        fields[key] = extract_value(related_property)
    if config.get("company_name"):
        related_company = getattr(obj.properties, config["company"], None)
        if related_company:
            related_company_object = related_company.fetch()
            if related_company_object:
                fields["company"] = getattr(
                    related_company.fetch().properties, config["company_name"]
                ).value
        else:
            fields["company"] = ""
    fields["lime_id"] = obj.id
    fields["limetype"] = obj.limetype.name
    return fields


def get_plugin_config(app):
    default_config = {
        "company": {"limetype": "company"},
        "coworker": {
            "limetype": "coworker",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "email",
            "mobile": "mobilephone",
        },
        "use_custom_config": False,
        "use_default_persons_object": False,
        "deal": {
            "get_persons_from_related_company": True,
            "dealSettings": [
                {"personFields": ["person"], "deal_value": "value", "limetype": "deal"}
            ],
        },
        "person": {
            "personSettings": [
                {
                    "use_for_search": True,
                    "limetype": "person",
                    "first_name": "firstname",
                    "last_name": "lastname",
                    "email": "email",
                    "mobile": "mobilephone",
                    "company": "company",
                    "company_name": "name",
                }
            ]
        },
        "documents": {"limetype": "document", "document_name": "comment"},
    }
    try:
        config = RuntimeConfig(application=app).get_config()

        if config.get("use_custom_config"):

            return config
        else:
            return default_config
    except Exception as e:
        print(e)
        bugsnag.notify(e)
        return default_config
