import { h } from "@stencil/core";
import { fetchDocumentDetails, removeDocument } from "../../services";
import moment from "moment/moment";
import { EnumViews } from "../../models/EnumViews";
import { EnumDocumentStatuses } from "../../models/EnumDocumentStatuses";
export class LayoutDocumentDetails {
    componentWillLoad() {
        this.loadDocumentDetails();
    }
    constructor() {
        this.documentId = undefined;
        this.platform = undefined;
        this.session = undefined;
        this.documentData = {};
        this.isLoading = false;
        this.removeDocumentHandler = this.removeDocumentHandler.bind(this);
        this.openDocumentIntGetAcceptHandler =
            this.openDocumentIntGetAcceptHandler.bind(this);
    }
    render() {
        return [
            h("div", { key: 'dfc6facad1fd9afbadcdc4ea6fee3183bfd6d3e3' }, h("h3", { key: '4791c570b7d23c24b59d100510aa29185f708d6c' }, "Document Details"), (() => {
                if (this.isLoading) {
                    return h("ga-loader", null);
                }
                else {
                    return (h("div", { class: "document-details-container" }, h("div", { class: "document-details-info" }, h("ul", { class: "document-details-info-list" }, h("li", null, h("span", { class: "document-detail-title" }, "Document name:"), ' ', this.documentData.name), h("li", null, h("span", { class: "document-detail-title" }, "Status:"), ' ', this.documentData.status), h("li", null, h("span", { class: "document-detail-title" }, "Deal value:"), ' ', this.documentData.value), h("li", null, h("span", { class: "document-detail-title" }, "Expiration date:"), ' ', this.documentData.expiration_date), h("li", null, h("span", { class: "document-detail-title" }, "Send date:"), ' ', this.documentData.send_date)), h("div", { class: "document-details-action-buttons" }, h("limel-button", { primary: true, label: "Open in GetAccept", onClick: this
                            .openDocumentIntGetAcceptHandler }), h("limel-button", { class: "document-details-action-button-remove", primary: false, label: "Remove document", onClick: this.removeDocumentHandler }))), h("div", { class: "document-details-pages" }, h("ul", null, this.documentData.pages.map(page => {
                        return (h("document-page-info", { documentId: this.documentData.id, session: this.session, page: page, totalTime: this.totalPageViewTime }));
                    })))));
                }
            })()),
        ];
    }
    async loadDocumentDetails() {
        // should load document details. Replace hard coded id with id from this.document.
        this.isLoading = true;
        const rawDocument = await fetchDocumentDetails(this.platform, this.session, this.documentId);
        this.documentData = {
            id: rawDocument.id,
            name: rawDocument.name,
            page_count: rawDocument.page_count,
            status: rawDocument.status,
            value: rawDocument.value,
            expiration_date: moment(rawDocument.expiration_date).format('YYYY-MM-DD'),
            send_date: this.getSendDate(rawDocument),
            pages: this.getDocumentPages(rawDocument),
        };
        this.totalPageViewTime = this.getTotalPageViewTime(rawDocument);
        this.isLoading = false;
    }
    getSendDate(rawDocument) {
        return ((rawDocument.send_date &&
            moment(rawDocument.send_date).format('YYYY-MM-DD')) ||
            '');
    }
    getDocumentPages(rawDocument) {
        return ((rawDocument.pages &&
            rawDocument.pages.map((page) => {
                return {
                    page_id: page.page_id,
                    thumb_url: page.thumb_url,
                    page_time: page.page_time,
                    order_num: page.order_num,
                    page_num: page.page_num,
                };
            })) ||
            []);
    }
    getTotalPageViewTime(rawDocument) {
        return ((rawDocument.pages &&
            rawDocument.pages.reduce((acc, page) => acc + page.page_time, 0)) ||
            0);
    }
    async removeDocumentHandler() {
        this.isLoading = true;
        const result = await removeDocument(this.platform, this.session, this.documentId);
        this.isLoading = false;
        if (result) {
            this.changeView.emit(EnumViews.home);
        }
    }
    openDocumentIntGetAcceptHandler() {
        const page = this.documentData.status === EnumDocumentStatuses.draft
            ? 'edit'
            : 'view';
        window.open(`https://app.getaccept.com/document/${page}/${this.documentData.id}`, '_blank');
    }
    static get is() { return "layout-document-details"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-document-details.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-document-details.css"]
        };
    }
    static get properties() {
        return {
            "documentId": {
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
                "attribute": "document-id",
                "reflect": false
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
            }
        };
    }
    static get states() {
        return {
            "documentData": {},
            "isLoading": {}
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
            }];
    }
}
//# sourceMappingURL=layout-document-details.js.map
