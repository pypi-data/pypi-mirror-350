import { h } from "@stencil/core";
const timeout = 10000;
export class DocumentList {
    constructor() {
        this.documents = [];
        this.intervalId = undefined;
    }
    componentWillLoad() {
        this.loadRelatedDocuments.emit();
        this.intervalId = setInterval(() => {
            this.loadRelatedDocuments.emit();
        }, timeout);
    }
    disconnectedCallback() {
        clearInterval(this.intervalId);
    }
    render() {
        if (!this.documents.length) {
            return h("empty-state", { text: "No documents were found!" });
        }
        return [
            h("ul", { class: "document-list" }, this.documents.map(document => {
                return h("document-list-item", { document: document });
            })),
        ];
    }
    static get is() { return "document-list"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["document-list.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["document-list.css"]
        };
    }
    static get properties() {
        return {
            "documents": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IDocument[]",
                    "resolved": "IDocument[]",
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
                },
                "defaultValue": "[]"
            }
        };
    }
    static get states() {
        return {
            "intervalId": {}
        };
    }
    static get events() {
        return [{
                "method": "loadRelatedDocuments",
                "name": "loadRelatedDocuments",
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
//# sourceMappingURL=document-list.js.map
