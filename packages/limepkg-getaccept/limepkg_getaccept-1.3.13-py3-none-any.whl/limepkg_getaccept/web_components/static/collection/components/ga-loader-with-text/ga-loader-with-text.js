import { h } from "@stencil/core";
export class GALoaderWithText {
    constructor() {
        this.showText = false;
        this.text = undefined;
    }
    render() {
        return (h("div", { key: '5892e446acdc6e3799e7efb332c0b996acfd77f0', class: "share-document-loading-container" }, (() => {
            if (this.showText) {
                return (h("div", null, h("h3", null, this.text)));
            }
        })(), h("ga-loader", { key: 'df4d0ac848c9f78f5e9f38eeff98122f3009b31d' })));
    }
    static get is() { return "ga-loader-with-text"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["ga-loader-with-text.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["ga-loader-with-text.css"]
        };
    }
    static get properties() {
        return {
            "showText": {
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
                "attribute": "show-text",
                "reflect": false,
                "defaultValue": "false"
            },
            "text": {
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
                "attribute": "text",
                "reflect": false
            }
        };
    }
}
//# sourceMappingURL=ga-loader-with-text.js.map
