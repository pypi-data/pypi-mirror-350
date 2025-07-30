import { h } from "@stencil/core";
export class DocumentErrorFeedback {
    constructor() {
        this.document = undefined;
        this.errorList = [];
    }
    render() {
        return [
            h("div", { key: '6518d28dabf6d7de6e4fd21ff5d86d187f437085' }, h("h3", { key: '08887413747c6a5ee7ea2cf91c5d03726d0c5020' }, "You need to fix following tasks to send:"), h("ul", { key: '3b81a34f6f1cac3e6984b601ce46b74382f2f421', class: "document-error-list" }, this.errorList.map(error => {
                return h("document-error", { error: error });
            }))),
        ];
    }
    static get is() { return "document-error-feedback"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["document-error-feedback.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["document-error-feedback.css"]
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
            },
            "errorList": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IError[]",
                    "resolved": "IError[]",
                    "references": {
                        "IError": {
                            "location": "import",
                            "path": "../../types/Error",
                            "id": "src/types/Error.ts::IError"
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
}
//# sourceMappingURL=document-error-feedback.js.map
