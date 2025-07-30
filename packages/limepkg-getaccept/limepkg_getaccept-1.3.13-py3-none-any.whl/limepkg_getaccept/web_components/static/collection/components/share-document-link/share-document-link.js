import { h } from "@stencil/core";
export class ShareDocumentLink {
    constructor() {
        this.recipient = undefined;
        this.handleCopyLink = this.handleCopyLink.bind(this);
    }
    render() {
        return (h("li", { key: '262815491c2a7ae7c2311acbb76e81335efa64fc', class: "share-document-list-item" }, h("div", { key: '64422961902488b16f6350ef39f69ba4a6923dee', class: "recipient-info-container" }, h("div", { key: '4169a8781fd0f2231ddcf5907a699cbbb2ab3757', class: "recipient-icon" }, h("limel-icon", { key: '6401d83e3a3efe3419eabce499cb4c55ae881b2d', name: "user", size: "small" })), h("div", { key: '9ba77fa755a0545b043972499ef1d70e9ea8a546', class: "recipient-info" }, h("span", { key: '9fc87e43ba13ee561e74bceb516d751308a86342', class: "recipient-info-name" }, this.recipient.fullname), h("span", { key: '4d59419a455516a99753c046108e849637e1f4eb', class: "recipient-info-role" }, this.recipient.role))), h("div", { key: '3920f52319f0ce4770b49a49cdf2080b82df0cdd' }, h("limel-input-field", { key: '3e2befb3a12d33f247edd483abe321d0e5ace93c', label: "Signing link", type: "email", value: this.recipient.document_url, trailingIcon: "copy_link", onAction: this.handleCopyLink }))));
    }
    handleCopyLink() {
        const copyText = document.createElement('textarea');
        copyText.value = this.recipient.document_url;
        document.body.appendChild(copyText);
        copyText.select();
        document.execCommand('copy');
        document.body.removeChild(copyText);
    }
    static get is() { return "share-document-link"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["share-document-link.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["share-document-link.css"]
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
            }
        };
    }
}
//# sourceMappingURL=share-document-link.js.map
