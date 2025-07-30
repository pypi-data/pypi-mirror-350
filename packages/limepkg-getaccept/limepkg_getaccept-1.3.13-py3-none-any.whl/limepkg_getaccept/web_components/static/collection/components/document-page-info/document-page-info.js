import { h } from "@stencil/core";
export class DocumentPageInfo {
    constructor() {
        this.page = undefined;
        this.documentId = undefined;
        this.session = undefined;
        this.totalTime = 0;
        this.value = 0;
        this.valuePercent = 0;
    }
    componentWillLoad() {
        if (this.totalTime > 0 && this.page.page_time > 0) {
            this.value = this.page.page_time / this.totalTime;
            // eslint-disable-next-line @typescript-eslint/no-magic-numbers
            this.valuePercent = Math.round(this.value * 100);
        }
    }
    getThumbUrl(originalUrl = '') {
        const s3_credentials = originalUrl.split('?')[1];
        const bucket = this.getS3Bucket(originalUrl);
        return `getaccept/page_thumb_proxy/${bucket}/${this.session.entity_id}/${this.documentId}/${this.page.page_id}/${encodeURIComponent(s3_credentials)}`;
    }
    getS3Bucket(originalUrl) {
        return originalUrl.replace('https://', '').split('.s3.')[0] || '';
    }
    render() {
        return [
            h("div", { key: '1d3054248e8cf8bd53de15b1c922a5201ba82d56', class: "page-info-container" }, h("div", { key: '429fb9abcc7a0380a90002eb57ce85f7ffd578d2', class: "page-number" }, this.page.page_num), h("img", { key: 'f9ef68b1f80e78dd9df84765a81418abab134b15', class: "page-thumb", src: this.getThumbUrl(this.page.thumb_url) }), h("div", { key: 'e327710c8b64fcd64e0a31f9aca483472505ffd8', class: "page-time-spent" }, h("span", { key: 'e6864382d6b843dae2109f8ac2607890ea8e16ae', class: "page-time-spent-text" }, "Time spent"), h("span", { key: '7ea3035fef4bcb9946f63fc5c0832f531f078100' }, this.page.page_time, "s"))),
            h("div", { key: '4d98632ee40d2f10e6ab6c5e514512cf15391ede', class: "page-info-percent" }, h("span", { key: '6c1130095b75166e80e3e20f22df6364ed23a9d2' }, this.valuePercent, "%"), h("limel-linear-progress", { key: '1028bfcfeea4f0e07868a81ecfbbbc96abcff17e', value: this.value })),
        ];
    }
    static get is() { return "document-page-info"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["document-page-info.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["document-page-info.css"]
        };
    }
    static get properties() {
        return {
            "page": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IDocumentPage",
                    "resolved": "IDocumentPage",
                    "references": {
                        "IDocumentPage": {
                            "location": "import",
                            "path": "../../types/DocumentPage",
                            "id": "src/types/DocumentPage.ts::IDocumentPage"
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
            "totalTime": {
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
                "attribute": "total-time",
                "reflect": false,
                "defaultValue": "0"
            }
        };
    }
    static get states() {
        return {
            "value": {},
            "valuePercent": {}
        };
    }
}
//# sourceMappingURL=document-page-info.js.map
