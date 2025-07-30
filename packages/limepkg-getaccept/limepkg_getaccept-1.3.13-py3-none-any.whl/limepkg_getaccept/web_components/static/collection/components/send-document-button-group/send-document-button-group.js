import { h } from "@stencil/core";
export class SendDocumentButtonGroup {
    constructor() {
        this.disabled = false;
        this.loading = false;
        this.handleOnClickSendButton = this.handleOnClickSendButton.bind(this);
    }
    render() {
        return [
            h("div", { key: 'c7c1a237f7c2035d9dffd56ea1818844ed8c1aee', class: "send-document-button-group" }, h("limel-button", { key: '673a56beed71d2a9d6b3e63f028071a0bdfe9119', label: "Prepare for sendout", primary: true, loading: this.loading, disabled: this.disabled, onClick: this.handleOnClickSendButton })),
        ];
    }
    handleOnClickSendButton() {
        this.validateDocument.emit();
    }
    static get is() { return "send-document-button-group"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["send-document-button-group.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["send-document-button-group.css"]
        };
    }
    static get states() {
        return {
            "disabled": {},
            "loading": {}
        };
    }
    static get events() {
        return [{
                "method": "validateDocument",
                "name": "validateDocument",
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
//# sourceMappingURL=send-document-button-group.js.map
