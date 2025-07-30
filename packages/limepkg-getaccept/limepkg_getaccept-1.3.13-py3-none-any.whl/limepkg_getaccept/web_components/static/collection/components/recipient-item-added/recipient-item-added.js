import { h } from "@stencil/core";
export class RecipientItemAdded {
    constructor() {
        this.roles = [];
        this.recipient = undefined;
        this.isSigning = undefined;
        this.handleChangeRole = this.handleChangeRole.bind(this);
        this.handleRemoveRecipient = this.handleRemoveRecipient.bind(this);
        this.selectedRole = this.selectedRole.bind(this);
    }
    componentWillLoad() {
        this.addRecipientRoles();
    }
    addRecipientRoles() {
        if (this.isSigning) {
            this.roles.push({
                value: 'signer',
                label: 'Signer',
            });
        }
        this.roles.push({
            value: 'cc',
            label: 'Viewer',
        }, {
            value: 'approver',
            label: 'Internal approver',
        }, {
            value: 'externalApprover',
            label: 'External approver',
        });
        if (!this.recipient.role) {
            this.recipient.role = this.roles[0].value;
            this.changeRecipientRole.emit(this.recipient);
        }
    }
    render() {
        const { fullname, email } = this.recipient;
        return (h("li", { key: '1de674ef777018a7ae86b1279c93222224a69286', class: "recipient-list-item" }, h("div", { key: 'ec2a82dab4008a9fc571d0cff673e9f4c165f4ae', class: "recipient-info-container" }, h("span", { key: 'bdb5317ddd3a284fdd75bc1807763a2dc4ade722' }, fullname), h("div", { key: 'f3104fdc1db174741fa1ede7b73480cf16bc9094', class: "recipient-info-contact-data" }, h("span", { key: '55a5d96b0704141b3fc162e3897204e0326c4a39' }, email))), h("div", { key: '15933045922782ebbaea98037d6af9626bbfa819', class: "recipient-role-container" }, h("select", { key: '59b33bd5388f4a30a157194c2740ff8912723c48', class: "recipient-role-list", onInput: event => this.handleChangeRole(event) }, this.roles.map(role => {
            return (h("option", { value: role.value, selected: this.selectedRole(role) }, role.label));
        }))), h("div", { key: '8a3630597d871e2f86ca3ba005fde755ff86deca', class: "recipient-remove-button", onClick: this.handleRemoveRecipient }, h("limel-icon", { key: '16e521d9329db35be7957bbafc241a3c31e456aa', name: "trash", size: "small" }))));
    }
    handleChangeRole(event) {
        this.recipient.role = event.target.value;
        this.changeRecipientRole.emit(this.recipient);
    }
    handleRemoveRecipient() {
        this.removeRecipient.emit(this.recipient);
    }
    selectedRole(role) {
        return this.recipient.role === role.value;
    }
    static get is() { return "recipient-item-added"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["recipient-item-added.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["recipient-item-added.css"]
        };
    }
    static get properties() {
        return {
            "recipient": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IRecipient",
                    "resolved": "IRecipient",
                    "references": {
                        "IRecipient": {
                            "location": "import",
                            "path": "../../types/Recipient",
                            "id": "src/types/Recipient.ts::IRecipient"
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
            "isSigning": {
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
                "attribute": "is-signing",
                "reflect": false
            }
        };
    }
    static get events() {
        return [{
                "method": "changeRecipientRole",
                "name": "changeRecipientRole",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "IRecipient",
                    "resolved": "IRecipient",
                    "references": {
                        "IRecipient": {
                            "location": "import",
                            "path": "../../types/Recipient",
                            "id": "src/types/Recipient.ts::IRecipient"
                        }
                    }
                }
            }, {
                "method": "removeRecipient",
                "name": "removeRecipient",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "IRecipient",
                    "resolved": "IRecipient",
                    "references": {
                        "IRecipient": {
                            "location": "import",
                            "path": "../../types/Recipient",
                            "id": "src/types/Recipient.ts::IRecipient"
                        }
                    }
                }
            }];
    }
}
//# sourceMappingURL=recipient-item-added.js.map
