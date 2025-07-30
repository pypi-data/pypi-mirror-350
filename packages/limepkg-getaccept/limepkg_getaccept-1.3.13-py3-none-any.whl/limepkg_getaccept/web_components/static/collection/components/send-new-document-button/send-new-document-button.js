import { h } from "@stencil/core";
import { EnumViews } from "../../models/EnumViews";
export class Root {
    buttonData() {
        if (this.isSigning) {
            return {
                label: 'Document for signing',
                icon: 'edit',
                description: 'Used for signing sales related documents.',
                buttonText: 'For signing',
            };
        }
        return {
            label: 'Document for tracking',
            icon: 'search',
            description: 'Used when no signing is required.',
            buttonText: 'For tracking',
        };
    }
    constructor() {
        this.isSigning = undefined;
        this.changeViewHandler = this.changeViewHandler.bind(this);
    }
    render() {
        let buttonContainer = 'new-document-button-container';
        buttonContainer += !this.isSigning ? ' tracking' : '';
        const { icon, label, buttonText, description } = this.buttonData();
        return [
            h("div", { key: '76564b2679feb299b86e95a44c8c5f01a9741b1a', class: buttonContainer }, h("h4", { key: 'd4c9e600ef12cf0d4a75723dd5b3706d3c794563' }, label), h("limel-icon", { key: '48b3e662d69feddb0e8d7f4666da24a3f0e7c28b', class: "new-document-icon", name: icon, size: "large" }), h("limel-button", { key: '643d103074abb058c64ab9dad650be8d8aa7d926', primary: true, label: buttonText, onClick: this.changeViewHandler }), h("p", { key: '2915fffe7bf47e5cd19909a951b3610980794564' }, description)),
        ];
    }
    changeViewHandler() {
        this.changeView.emit(EnumViews.recipient);
        this.setDocumentType.emit(this.isSigning);
    }
    static get is() { return "send-new-document-button"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["send-new-document-button.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["send-new-document-button.css"]
        };
    }
    static get properties() {
        return {
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
                    "original": "any",
                    "resolved": "any",
                    "references": {}
                }
            }, {
                "method": "setDocumentType",
                "name": "setDocumentType",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "boolean",
                    "resolved": "boolean",
                    "references": {}
                }
            }];
    }
}
//# sourceMappingURL=send-new-document-button.js.map
