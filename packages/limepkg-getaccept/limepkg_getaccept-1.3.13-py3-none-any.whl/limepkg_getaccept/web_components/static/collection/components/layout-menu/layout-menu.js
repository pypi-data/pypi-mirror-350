import { h } from "@stencil/core";
import { EnumViews } from "../../models/EnumViews";
export class LayoutMenu {
    constructor() {
        this.activeView = undefined;
        this.isSending = undefined;
        this.menuItems = [
            {
                text: 'Help',
                icon: 'ask_question',
                value: EnumViews.help,
            },
            {
                text: 'Settings',
                icon: 'settings',
                value: EnumViews.settings,
            },
            {
                text: 'Logout',
                icon: 'exit',
                value: EnumViews.logout,
            },
        ];
        this.isOpen = false;
        this.toggleMenu = this.toggleMenu.bind(this);
        this.handleBack = this.handleBack.bind(this);
        this.showBackButton = this.showBackButton.bind(this);
        this.previousViewOnClose = this.previousViewOnClose.bind(this);
        this.onNavigate = this.onNavigate.bind(this);
        this.onCancelMenu = this.onCancelMenu.bind(this);
    }
    render() {
        if (this.isSending) {
            return [];
        }
        if (this.showBackButton()) {
            return (h("limel-button", { class: "ga-menu", onClick: this.handleBack, label: "Back" }));
        }
        return (h("limel-menu", { class: "ga-menu", items: this.menuItems, onCancel: this.onCancelMenu, onSelect: this.onNavigate, open: this.isOpen }, h("div", { slot: "trigger" }, h("limel-icon-button", { icon: "menu", onClick: this.toggleMenu }))));
    }
    toggleMenu() {
        this.isOpen = !this.isOpen;
    }
    handleBack() {
        this.changeView.emit(this.previousViewOnClose());
    }
    onNavigate(event) {
        this.changeView.emit(event.detail.value);
        this.isOpen = false;
    }
    onCancelMenu() {
        this.isOpen = false;
    }
    previousViewOnClose() {
        switch (this.activeView) {
            case EnumViews.videoLibrary:
                return EnumViews.sendDocument;
            case EnumViews.invite:
                return EnumViews.home;
            case EnumViews.help:
                return EnumViews.home;
            case EnumViews.settings:
                return EnumViews.home;
            case EnumViews.documentDetail:
                return EnumViews.home;
            case EnumViews.documentValidation:
                return EnumViews.sendDocument;
            default:
                return this.activeView;
        }
    }
    showBackButton() {
        switch (this.activeView) {
            case EnumViews.videoLibrary:
                return true;
            case EnumViews.invite:
                return true;
            case EnumViews.help:
                return true;
            case EnumViews.settings:
                return true;
            case EnumViews.documentDetail:
                return true;
            case EnumViews.documentValidation:
                return false;
            default:
                return false;
        }
    }
    static get is() { return "layout-menu"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-menu.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-menu.css"]
        };
    }
    static get properties() {
        return {
            "activeView": {
                "type": "string",
                "mutable": false,
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
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "active-view",
                "reflect": false
            },
            "isSending": {
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
                "attribute": "is-sending",
                "reflect": false
            }
        };
    }
    static get states() {
        return {
            "menuItems": {},
            "isOpen": {}
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
//# sourceMappingURL=layout-menu.js.map
