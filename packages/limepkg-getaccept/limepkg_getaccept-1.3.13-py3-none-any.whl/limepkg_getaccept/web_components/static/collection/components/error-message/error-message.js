import { h } from "@stencil/core";
export class ErrorMessage {
    constructor() {
        this.timeout = 10000;
        this.error = '';
        this.message = '';
        this.triggerSnackbar = this.triggerSnackbar.bind(this);
    }
    componentDidUpdate() {
        if (this.error) {
            this.message = this.error;
            this.triggerSnackbar();
        }
    }
    render() {
        return [
            h("limel-snackbar", { key: '5e532184678b3be9ba2e97e503ca78815189ae1d', message: this.message, timeout: this.timeout, actionText: "Ok" }),
        ];
    }
    triggerSnackbar() {
        const snackbar = this.host.shadowRoot.querySelector('limel-snackbar');
        snackbar.show();
    }
    static get is() { return "error-message"; }
    static get encapsulation() { return "shadow"; }
    static get properties() {
        return {
            "timeout": {
                "type": "number",
                "mutable": false,
                "complexType": {
                    "original": "number",
                    "resolved": "number",
                    "references": {}
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "timeout",
                "reflect": false,
                "defaultValue": "10000"
            },
            "error": {
                "type": "string",
                "mutable": false,
                "complexType": {
                    "original": "string",
                    "resolved": "string",
                    "references": {}
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "error",
                "reflect": false,
                "defaultValue": "''"
            }
        };
    }
    static get states() {
        return {
            "message": {}
        };
    }
    static get elementRef() { return "host"; }
}
//# sourceMappingURL=error-message.js.map
