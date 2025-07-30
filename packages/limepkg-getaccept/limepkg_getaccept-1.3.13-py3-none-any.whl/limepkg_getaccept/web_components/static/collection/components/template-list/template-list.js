import { h } from "@stencil/core";
export class TemplateList {
    constructor() {
        this.templates = undefined;
        this.selectedTemplate = undefined;
        this.isLoading = undefined;
        this.selectTemplate = this.selectTemplate.bind(this);
    }
    render() {
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        if (!this.templates.length) {
            return h("empty-state", { text: "No templates were found!" });
        }
        return (h("limel-list", { class: "accordion-content", items: this.templates, type: "selectable", onChange: this.selectTemplate }));
    }
    selectTemplate(event) {
        this.setTemplate.emit(event.detail);
    }
    static get is() { return "template-list"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["template-list.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["template-list.css"]
        };
    }
    static get properties() {
        return {
            "templates": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "Array<ListItem | ListSeparator>",
                    "resolved": "(ListSeparator | ListItem<any>)[]",
                    "references": {
                        "Array": {
                            "location": "global",
                            "id": "global::Array"
                        },
                        "ListItem": {
                            "location": "import",
                            "path": "@limetech/lime-elements",
                            "id": ""
                        },
                        "ListSeparator": {
                            "location": "import",
                            "path": "@limetech/lime-elements",
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
            "selectedTemplate": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IListItem",
                    "resolved": "IListItem",
                    "references": {
                        "IListItem": {
                            "location": "import",
                            "path": "../../types/ListItem",
                            "id": "src/types/ListItem.ts::IListItem"
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
            "isLoading": {
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
                "attribute": "is-loading",
                "reflect": false
            }
        };
    }
    static get events() {
        return [{
                "method": "setTemplate",
                "name": "setTemplate",
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
//# sourceMappingURL=template-list.js.map
