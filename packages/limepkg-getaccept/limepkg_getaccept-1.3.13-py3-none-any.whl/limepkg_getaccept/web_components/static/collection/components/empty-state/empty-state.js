import { h } from "@stencil/core";
export class EmptyState {
    constructor() {
        this.text = undefined;
        this.icon = 'nothing_found';
    }
    render() {
        return (h("div", { key: 'a230f0b89003280afd8206eebb77c5b5b8cd22f2', class: "empty-state" }, h("limel-icon", { key: 'fd224beccacb08c0294787687fe7b40327feb5b9', name: this.icon }), h("p", { key: '84e9d511f1eb14a1bd5b3ac6f75d1c76cc15f63b' }, this.text)));
    }
    static get is() { return "empty-state"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["empty-state.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["empty-state.css"]
        };
    }
    static get properties() {
        return {
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
            },
            "icon": {
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
                "attribute": "icon",
                "reflect": false,
                "defaultValue": "'nothing_found'"
            }
        };
    }
}
//# sourceMappingURL=empty-state.js.map
