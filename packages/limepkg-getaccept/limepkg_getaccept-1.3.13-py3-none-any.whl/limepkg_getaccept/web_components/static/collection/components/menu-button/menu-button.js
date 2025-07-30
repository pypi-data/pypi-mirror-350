import { h } from "@stencil/core";
export class MenuButton {
    constructor() {
        this.menuItem = undefined;
        this.handleMenuClick = this.handleMenuClick.bind(this);
    }
    render() {
        const { icon, label, view } = this.menuItem;
        return (h("li", { key: '947319378e0021a2e06223c6eb325011b200d99f', class: "ga-menu-item", onClick: () => this.handleMenuClick(view) }, h("limel-icon", { key: '95b2adf0cc36259544a6baccfbf5006f5a95fdcc', class: "menu-icon", name: icon, size: "small" }), h("span", { key: '986bc65df73709dd726a19512f5fd8c64f6e70ad' }, label)));
    }
    handleMenuClick(view) {
        this.changeView.emit(view);
        this.closeMenu.emit(false);
    }
    static get is() { return "menu-button"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["menu-button.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["menu-button.css"]
        };
    }
    static get properties() {
        return {
            "menuItem": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IMenuItem",
                    "resolved": "IMenuItem",
                    "references": {
                        "IMenuItem": {
                            "location": "import",
                            "path": "../../types/MenuItem",
                            "id": "src/types/MenuItem.ts::IMenuItem"
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
                    "original": "any",
                    "resolved": "any",
                    "references": {}
                }
            }, {
                "method": "closeMenu",
                "name": "closeMenu",
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
//# sourceMappingURL=menu-button.js.map
