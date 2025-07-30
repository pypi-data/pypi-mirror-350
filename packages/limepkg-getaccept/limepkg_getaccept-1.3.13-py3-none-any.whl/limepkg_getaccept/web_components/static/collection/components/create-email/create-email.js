import { h } from "@stencil/core";
export class CreateEmail {
    componentWillLoad() {
        this.emailSubject = this.document.email_send_subject;
        this.emailMessage = this.document.email_send_message;
    }
    constructor() {
        this.document = undefined;
        this.emailSubject = '';
        this.emailMessage = '';
        this.handleChangeEmailSubject =
            this.handleChangeEmailSubject.bind(this);
        this.handleChangeEmailMessage =
            this.handleChangeEmailMessage.bind(this);
    }
    render() {
        return [
            h("div", { key: '1d5599e24eb0c74fc2c258d17dd4bd663d83e3c2' }, h("h3", { key: '691a738cc762ba2b7254895120d3730275c939d7' }, "Write your email"), h("limel-input-field", { key: 'dcefe2d64ff7ad88cff2f446855ab8a961495eca', label: "Subject", value: this.emailSubject, onChange: this.handleChangeEmailSubject }), h("span", { key: 'b9437369529832f80081e9e4fa1dd86497ae33b6', class: "send-document-email-subject" }, "Email"), h("textarea", { key: '8b4f347aaa67bfbe405d7f82037f0268fa31fad3', class: "send-document-email", rows: 9, value: this.emailMessage, onChange: this.handleChangeEmailMessage })),
        ];
    }
    handleChangeEmailSubject(event) {
        this.emailSubject = event.detail;
        this.setEmailSubject.emit(event.detail);
    }
    handleChangeEmailMessage(event) {
        this.setEmailMessage.emit(event.target.value);
    }
    static get is() { return "create-email"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["create-email.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["create-email.css"]
        };
    }
    static get properties() {
        return {
            "document": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IDocument",
                    "resolved": "IDocument",
                    "references": {
                        "IDocument": {
                            "location": "import",
                            "path": "../../types/Document",
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
            }
        };
    }
    static get states() {
        return {
            "emailSubject": {},
            "emailMessage": {}
        };
    }
    static get events() {
        return [{
                "method": "setEmailSubject",
                "name": "setEmailSubject",
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
            }, {
                "method": "setEmailMessage",
                "name": "setEmailMessage",
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
//# sourceMappingURL=create-email.js.map
