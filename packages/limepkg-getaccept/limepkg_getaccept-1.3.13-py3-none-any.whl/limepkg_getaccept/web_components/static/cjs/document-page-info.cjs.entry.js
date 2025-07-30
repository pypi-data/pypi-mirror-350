'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const documentPageInfoCss = ".page-info-container{display:flex}.page-info-container .page-number{display:inline-flex;align-items:center;justify-content:center;height:1.5rem;width:1.5rem;margin-right:1rem;border-radius:50%;-webkit-border-radius:50%;-moz-border-radius:50%;-ms-border-radius:50%;-o-border-radius:50%;background-color:#f49132;color:#fff}.page-info-container .page-thumb{width:4rem;height:6rem;background-color:#ccc;object-fit:contain}.page-info-container .page-time-spent{margin-left:1rem}.page-info-container .page-time-spent .page-time-spent-text{display:block;font-size:0.6rem;font-weight:bold;text-transform:uppercase}.page-info-percent{margin-bottom:1rem}";
const DocumentPageInfoStyle0 = documentPageInfoCss;

const DocumentPageInfo = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
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
            index.h("div", { key: '1d3054248e8cf8bd53de15b1c922a5201ba82d56', class: "page-info-container" }, index.h("div", { key: '429fb9abcc7a0380a90002eb57ce85f7ffd578d2', class: "page-number" }, this.page.page_num), index.h("img", { key: 'f9ef68b1f80e78dd9df84765a81418abab134b15', class: "page-thumb", src: this.getThumbUrl(this.page.thumb_url) }), index.h("div", { key: 'e327710c8b64fcd64e0a31f9aca483472505ffd8', class: "page-time-spent" }, index.h("span", { key: 'e6864382d6b843dae2109f8ac2607890ea8e16ae', class: "page-time-spent-text" }, "Time spent"), index.h("span", { key: '7ea3035fef4bcb9946f63fc5c0832f531f078100' }, this.page.page_time, "s"))),
            index.h("div", { key: '4d98632ee40d2f10e6ab6c5e514512cf15391ede', class: "page-info-percent" }, index.h("span", { key: '6c1130095b75166e80e3e20f22df6364ed23a9d2' }, this.valuePercent, "%"), index.h("limel-linear-progress", { key: '1028bfcfeea4f0e07868a81ecfbbbc96abcff17e', value: this.value })),
        ];
    }
};
DocumentPageInfo.style = DocumentPageInfoStyle0;

exports.document_page_info = DocumentPageInfo;

//# sourceMappingURL=document-page-info.cjs.entry.js.map