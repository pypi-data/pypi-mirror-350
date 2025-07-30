import { h } from "@stencil/core";
export class LimeDocumentList {
    constructor() {
        this.documents = [];
        this.selectedLimeDocument = undefined;
        this.isLoading = undefined;
        this.selectDocument = this.selectDocument.bind(this);
    }
    render() {
        console.log(this.documents);
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        else if (!this.documents.length) {
            return h("empty-state", { text: "No documents were found!" });
        }
        return (h("limel-list", { class: "accordion-content", items: this.documents, type: "selectable", onChange: this.selectDocument }));
    }
    selectDocument(event) {
        this.setLimeDocument.emit(event.detail);
    }
    static get is() { return "lime-document-list"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["lime-document-list.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["lime-document-list.css"]
        };
    }
    static get properties() {
        return {
            "documents": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "any[]",
                    "resolved": "any[]",
                    "references": {}
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "defaultValue": "[]"
            },
            "selectedLimeDocument": {
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
                "method": "setLimeDocument",
                "name": "setLimeDocument",
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
//# sourceMappingURL=lime-document-list.js.map
