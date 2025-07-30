import { h } from "@stencil/core";
export class CustomFields {
    constructor() { this.template = undefined; this.customFields = undefined; this.isLoading = undefined; }
    render() {
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        else if (!this.template) {
            return [];
        }
        if (!this.customFields.length) {
            return [
                h("h4", null, "Fields"),
                h("empty-state", { text: "This template has no fields", icon: "text_box" }),
            ];
        }
        return [
            h("h4", null, "Fields"),
            this.customFields.map(field => (h("limel-input-field", { class: "custom-field", label: field.label, value: field.value, disabled: !field.is_editable, onChange: event => this.onChangeField(event, field.id) }))),
        ];
    }
    onChangeField(event, id) {
        this.updateFieldValue.emit({ id: id, value: event.detail });
    }
    static get is() { return "custom-fields"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["custom-fields.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["custom-fields.css"]
        };
    }
    static get properties() {
        return {
            "template": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IListItem",
                    "resolved": "IListItem",
                    "references": {
                        "IListItem": {
                            "location": "import",
                            "path": "../../types/ListItem",
                            "id": "src/types/ListItem.ts::IListItem"
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                }
            },
            "customFields": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "ICustomField[]",
                    "resolved": "ICustomField[]",
                    "references": {
                        "ICustomField": {
                            "location": "import",
                            "path": "../../types/CustomField",
                            "id": "src/types/CustomField.ts::ICustomField"
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                }
            },
            "isLoading": {
                "type": "boolean",
                "mutable": false,
                "complexType": {
                    "original": "boolean",
                    "resolved": "boolean",
                    "references": {}
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "is-loading",
                "reflect": false
            }
        };
    }
    static get events() {
        return [{
                "method": "updateFieldValue",
                "name": "updateFieldValue",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "any",
                    "resolved": "any",
                    "references": {}
                }
            }];
    }
}
//# sourceMappingURL=custom-fields.js.map
