import { h } from "@stencil/core";
export class SelectedRecipientList {
    constructor() {
        this.recipients = undefined;
        this.document = undefined;
    }
    render() {
        if (!this.recipients.length) {
            return (h("empty-state", { icon: "user", text: "No recipients added. Find and add recipients to the left!" }));
        }
        return (h("ul", { class: "recipient-list" }, this.recipients.map(selectedRecipient => {
            return (h("recipient-item-added", { recipient: selectedRecipient, isSigning: this.document.is_signing }));
        })));
    }
    static get is() { return "selected-recipient-list"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["selected-recipient-list.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["selected-recipient-list.css"]
        };
    }
    static get properties() {
        return {
            "recipients": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IRecipient[]",
                    "resolved": "IRecipient[]",
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
}
//# sourceMappingURL=selected-recipient-list.js.map
