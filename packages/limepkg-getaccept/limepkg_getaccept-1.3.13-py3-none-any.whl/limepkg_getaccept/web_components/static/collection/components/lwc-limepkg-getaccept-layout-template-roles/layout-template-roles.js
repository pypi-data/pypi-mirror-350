import { h } from "@stencil/core";
import { EnumViews } from "../../models/EnumViews";
const roleNames = {
    signer: 'Signer',
    approver: 'Internal approver',
    externalApprover: 'External approver',
    cc: 'Viewer',
};
export class LayoutTemplateRoles {
    constructor() {
        this.context = undefined;
        this.document = undefined;
        this.template = undefined;
        this.limeDocument = undefined;
        this.platform = undefined;
        this.session = undefined;
        this.templateRoles = [];
        this.value = [];
        this.options = undefined;
        this.recipients = undefined;
        this.getOptions = this.getOptions.bind(this);
        this.getRecipientByOption = this.getRecipientByOption.bind(this);
    }
    get roles() {
        return this.templateRoles.filter(role => !this.isRecipient(role));
    }
    componentWillLoad() {
        if (!this.templateRoles.length) {
            this.changeView.emit(EnumViews.sendDocument);
        }
        this.recipients = this.document.recipients;
        this.options = this.recipients.map(recipient => ({
            text: recipient.fullname,
            value: recipient.email,
        }));
        this.value = Array(this.roles.length);
        this.roles.forEach((role, index) => {
            const relatedRecipient = this.recipients.find(recipient => recipient.role_id === role.role_id);
            if (relatedRecipient) {
                this.value[index] = {
                    text: relatedRecipient.fullname,
                    value: relatedRecipient.email,
                };
            }
        });
    }
    getRecipientByOption(option) {
        return this.recipients.find(recipient => recipient.fullname === option.text &&
            recipient.email === option.value);
    }
    getOptions(roleName) {
        return this.options.filter(option => !this.value.map(value => value === null || value === void 0 ? void 0 : value.value).includes(option.value) &&
            this.getRecipientByOption(option).role === roleName);
    }
    render() {
        return (h("section", { key: 'c25354902dcc6f433d522f39a20694de61922db3', class: "template-roles" }, this.roles.map((role, index) => {
            return (h("div", { class: "template-roles__column" }, h("limel-select", { label: `${roleNames[role.role]} - ${role.role_name}`, value: this.value[index], options: this.getOptions(role.role), onChange: event => this.handleChange(event, index, role) })));
        })));
    }
    isRecipient(role) {
        return !!role.first_name || !!role.last_name || !!role.email;
    }
    handleChange(event, index, role) {
        this.value[index] = event.detail;
        this.value = [...this.value];
        this.recipientRoleUpdated.emit({
            recipient: this.getRecipientByOption(event.detail),
            role: role,
        });
    }
    static get is() { return "layout-template-roles"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-template-roles.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-template-roles.css"]
        };
    }
    static get properties() {
        return {
            "context": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "LimeWebComponentContext",
                    "resolved": "LimeWebComponentContext",
                    "references": {
                        "LimeWebComponentContext": {
                            "location": "import",
                            "path": "@limetech/lime-web-components",
                            "id": ""
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": "The context this component belongs to"
                }
            },
            "document": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IDocument",
                    "resolved": "IDocument",
                    "references": {
                        "IDocument": {
                            "location": "import",
                            "path": "src/types/Document",
                            "id": "src/types/Document.ts::IDocument"
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
            "template": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IListItem",
                    "resolved": "IListItem",
                    "references": {
                        "IListItem": {
                            "location": "import",
                            "path": "src/types/ListItem",
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
            "limeDocument": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IListItem",
                    "resolved": "IListItem",
                    "references": {
                        "IListItem": {
                            "location": "import",
                            "path": "src/types/ListItem",
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
            "platform": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "LimeWebComponentPlatform",
                    "resolved": "LimeWebComponentPlatform",
                    "references": {
                        "LimeWebComponentPlatform": {
                            "location": "import",
                            "path": "@limetech/lime-web-components",
                            "id": ""
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": "Reference to the platform"
                }
            },
            "session": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "ISession",
                    "resolved": "ISession",
                    "references": {
                        "ISession": {
                            "location": "import",
                            "path": "src/types/Session",
                            "id": "src/types/Session.ts::ISession"
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
            "templateRoles": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "ITemplateRole[]",
                    "resolved": "ITemplateRole[]",
                    "references": {
                        "ITemplateRole": {
                            "location": "import",
                            "path": "src/types/TemplateRole",
                            "id": "src/types/TemplateRole.ts::ITemplateRole"
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "defaultValue": "[]"
            }
        };
    }
    static get states() {
        return {
            "value": {},
            "options": {},
            "recipients": {}
        };
    }
    static get events() {
        return [{
                "method": "recipientRoleUpdated",
                "name": "recipientRoleUpdated",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "{\n        recipient: IRecipient;\n        role: ITemplateRole;\n    }",
                    "resolved": "{ recipient: IRecipient; role: ITemplateRole; }",
                    "references": {
                        "IRecipient": {
                            "location": "import",
                            "path": "src/types/Recipient",
                            "id": "src/types/Recipient.ts::IRecipient"
                        },
                        "ITemplateRole": {
                            "location": "import",
                            "path": "src/types/TemplateRole",
                            "id": "src/types/TemplateRole.ts::ITemplateRole"
                        }
                    }
                }
            }, {
                "method": "changeView",
                "name": "changeView",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "EnumViews",
                    "resolved": "EnumViews.documentDetail | EnumViews.documentValidation | EnumViews.help | EnumViews.home | EnumViews.invite | EnumViews.login | EnumViews.logout | EnumViews.recipient | EnumViews.selectFile | EnumViews.sendDocument | EnumViews.settings | EnumViews.templateRoles | EnumViews.videoLibrary",
                    "references": {
                        "EnumViews": {
                            "location": "import",
                            "path": "../../models/EnumViews",
                            "id": "src/models/EnumViews.ts::EnumViews"
                        }
                    }
                }
            }];
    }
}
//# sourceMappingURL=layout-template-roles.js.map
