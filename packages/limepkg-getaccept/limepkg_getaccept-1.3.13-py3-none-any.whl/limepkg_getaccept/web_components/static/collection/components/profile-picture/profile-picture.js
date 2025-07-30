import { h } from "@stencil/core";
export class LayoutSettings {
    constructor() {
        this.thumbUrl = undefined;
    }
    render() {
        if (this.thumbUrl) {
            return (h("img", { class: "thumbnail", src: this.getThumbUrl(this.thumbUrl) }));
        }
        return (h("div", { class: "thumbnail thumbnail-placeholder" }, h("limel-icon", { name: "user" })));
    }
    getThumbUrl(originalUrl = '') {
        const path = originalUrl.split('/').slice(-1)[0];
        const urlPath = originalUrl.split('/')[3];
        return `getaccept/thumb_proxy/${urlPath}/${path}`;
    }
    static get is() { return "profile-picture"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["profile-picture.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["profile-picture.css"]
        };
    }
    static get properties() {
        return {
            "thumbUrl": {
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
                "attribute": "thumb-url",
                "reflect": false
            }
        };
    }
}
//# sourceMappingURL=profile-picture.js.map
