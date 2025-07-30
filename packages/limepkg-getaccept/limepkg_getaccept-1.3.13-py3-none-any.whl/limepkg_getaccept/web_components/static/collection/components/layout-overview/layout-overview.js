import { h } from "@stencil/core";
export class LayoutOverview {
    constructor() {
        this.sentDocuments = undefined;
        this.platform = undefined;
        this.externalId = undefined;
        this.session = undefined;
        this.documents = [];
        this.isAside = undefined;
        this.isLoadingDocuments = undefined;
    }
    render() {
        return [
            h("div", { key: 'e7aa2738d9da8ced2752ec1ea6ec4a81c3e7665c', class: { 'main-layout': true, aside: this.isAside } }, h("div", { key: '63922443f5e9a2f10431084200172a2401f4da31', class: "send-new-document-container" }, h("h3", { key: '2200c5727843da3bc118452bb1351a2a4b5b5f7c' }, "Send new document"), h("div", { key: 'e8e84c0418ba639c35857931753bbce8aadb8d53', class: "send-new-document-buttons" }, h("send-new-document-button", { key: 'f3be1a0062a77ecde18d66f8b9bbfa9a896b1f80', isSigning: true }), h("send-new-document-button", { key: 'a59e3b2336f303e7dc7f7902a6ac4167f3c1c1f1', isSigning: false }))), h("div", { key: 'aa32fe4f2bf0f0beb7f21859ab33c7ea7fd643ee', class: "related-documents" }, h("h3", { key: 'ccc0db40752c30b7c9a850283d546d82de0434fa' }, "Related documents"), this.isLoadingDocuments ? (h("ga-loader", null)) : (h("document-list", { documents: this.documents })))),
        ];
    }
    static get is() { return "layout-overview"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-overview.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-overview.css"]
        };
    }
    static get properties() {
        return {
            "sentDocuments": {
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
                    "text": ""
                }
            },
            "externalId": {
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
                "attribute": "external-id",
                "reflect": false
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
                            "path": "../../types/Session",
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
            },
            "isAside": {
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
                "attribute": "is-aside",
                "reflect": false
            }
        };
    }
    static get states() {
        return {
            "isLoadingDocuments": {}
        };
    }
}
//# sourceMappingURL=layout-overview.js.map
