import { h } from "@stencil/core";
import { EnumDocumentStatuses } from "../../models/EnumDocumentStatuses";
import moment from "moment";
export class DocumentListItem {
    constructor() {
        this.document = undefined;
        this.handleOpenDocument = this.handleOpenDocument.bind(this);
    }
    render() {
        const documentIcon = this.document.status.toLowerCase() + ' document-icon';
        return (h("li", { key: '9911c5fed8ca018bd54ea4251d7151a5f7f145f3', class: "document-list-item", onClick: this.handleOpenDocument }, h("div", { key: '2141cb39aebc77c27645cb6c889dd33011f179c8', class: documentIcon }, h("limel-icon", { key: '21ec366143a004844961cf4b25c0d8fba9fce3ce', name: this.getDocumentIcon(this.document.status), size: "small" })), h("div", { key: '6ece6e1cfd9b31f772aa9d3daeef0fb57ff70ef8', class: "document-info-container" }, h("div", { key: 'eaeca84bdd39cd60c414dc8a6f30e2d9b92edbb0', class: "document-name" }, this.document.name), h("div", { key: 'e364b5dc5954767e939979a42fe78a38c6fe7fc5', class: "document-status" }, h("span", { key: '87a97a5892d51847e14680c16b72d64c4ade431b' }, this.document.status), h("span", { key: '16ad9541ed13094e3209621fa7ba4ea99b948559', class: "document-created-date" }, moment(this.document.created_at).format('YYYY-MM-DD'))))));
    }
    handleOpenDocument() {
        this.openDocument.emit(this.document);
    }
    getDocumentIcon(status) {
        switch (status) {
            case EnumDocumentStatuses.draft:
                return 'no_edit';
            case EnumDocumentStatuses.hardbounced:
                return 'error';
            case EnumDocumentStatuses.importing:
                return 'import';
            case EnumDocumentStatuses.lost:
                return 'drama';
            case EnumDocumentStatuses.processing:
                return 'submit_progress';
            case EnumDocumentStatuses.recalled:
                return 'double_left';
            case EnumDocumentStatuses.rejected:
                return 'private';
            case EnumDocumentStatuses.reviewed:
                return 'preview_pane';
            case EnumDocumentStatuses.scheduled:
                return 'overtime';
            case EnumDocumentStatuses.sealed:
                return 'lock';
            case EnumDocumentStatuses.sent:
                return 'wedding_gift';
            case EnumDocumentStatuses.signed:
                return 'autograph';
            case EnumDocumentStatuses.signedwithoutverification:
                return 'autograph';
            case EnumDocumentStatuses.viewed:
                return 'visible';
            default:
                return 'dancing_party';
        }
    }
    static get is() { return "document-list-item"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["document-list-item.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["document-list-item.css"]
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
    static get events() {
        return [{
                "method": "openDocument",
                "name": "openDocument",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
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
                }
            }];
    }
}
//# sourceMappingURL=document-list-item.js.map
