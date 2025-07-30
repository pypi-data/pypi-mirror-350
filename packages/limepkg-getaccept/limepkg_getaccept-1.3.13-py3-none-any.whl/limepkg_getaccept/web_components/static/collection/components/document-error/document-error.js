import { h } from "@stencil/core";
export class DocumentError {
    constructor() {
        this.error = undefined;
        this.onClick = this.onClick.bind(this);
    }
    render() {
        return [
            h("li", { key: '1d6a9cf797eed8b633582cc876222c20c024de3e', class: "document-error", onClick: this.onClick }, h("div", { key: '10814c60ec0836b8ee4603ae5effbbf0797797b7', class: "document-error-icon" }, h("limel-icon", { key: 'e606522cdc5f883ded312e1dda78ab146fc01e65', name: this.error.icon, size: "small" })), h("div", { key: 'f2c94b009ff5d804fa17e196417a95e3cb9d5941', class: "document-error-info" }, h("h4", { key: '759344c7fa229dbb12fb4b3fae43fb6fb9c9be86', class: "document-error-header" }, this.error.header), h("span", { key: 'af468ae5684b16943020a9a4c82008148921c0d0' }, this.error.title))),
        ];
    }
    onClick() {
        this.changeView.emit(this.error.view);
    }
    static get is() { return "document-error"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["document-error.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["document-error.css"]
        };
    }
    static get properties() {
        return {
            "error": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IError",
                    "resolved": "IError",
                    "references": {
                        "IError": {
                            "location": "import",
                            "path": "../../types/Error",
                            "id": "src/types/Error.ts::IError"
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
                    "original": "EnumViews",
                    "resolved": "EnumViews.documentDetail | EnumViews.documentValidation | EnumViews.help | EnumViews.home | EnumViews.invite | EnumViews.login | EnumViews.logout | EnumViews.recipient | EnumViews.selectFile | EnumViews.sendDocument | EnumViews.settings | EnumViews.templateRoles | EnumViews.videoLibrary",
                    "references": {
                        "EnumViews": {
                            "location": "import",
                            "path": "../../models/EnumViews",
                            "id": "src/models/EnumViews.ts::EnumViews"
                        }
                    }
                }
            }];
    }
}
//# sourceMappingURL=document-error.js.map
