import { h } from "@stencil/core";
export class RecipientItem {
    constructor() {
        this.recipient = undefined;
        this.showAdd = true;
    }
    render() {
        const { fullname, email, mobile, limetype, company } = this.recipient;
        const icon = this.getIcon(limetype);
        const recipientList = `recipient-list-item ${this.isDisabled()}`;
        const contactInfoClasses = `recipient-info-contact-data${email ? ' contact--email' : ''}${mobile ? ' contact--phone' : ''}`;
        return (h("li", { key: 'f609cc55a44ceed4496c90b771dca943838142e1', class: recipientList }, h("div", { key: 'ab01cf1750386a95d1e2445fb8287ae9d274b466', class: `recipient-icon ${limetype}` }, h("limel-icon", { key: '755f8e0996fe24bf84fe22863e187872da532ddb', name: icon, size: "small" })), h("div", { key: 'ba92dc49d9a2cfcff472a5fdba3860df5e12ab0d', class: "recipient-info-container" }, h("span", { key: '79bd822952e430636af944844664a1445746ae3c' }, fullname), h("div", { key: 'cb38ca2bd58a20c15569c6fc50c07c3f4e3c1467' }, h("span", { key: 'ecc7b77e9eca8cb8f83b7e2a3946c2046fcb6e19' }, company)), h("div", { key: 'b6c8aee21a3873dd921810d2040d6e98b2165d48', class: contactInfoClasses }, h("span", { key: 'b2a1eb14eee12f84f673d121ae83fa8d74babfb6', class: "recipient-email" }, email), h("span", { key: '88f86646a77c0fa36a63066a289007053174e1b8', class: "recipient-phone" }, mobile))), this.renderAddIcon(this.showAdd)));
    }
    renderAddIcon(show) {
        return show ? (h("div", { class: "recipient-add-button" }, h("limel-icon", { name: "add", size: "medium" }))) : ([]);
    }
    getIcon(limetype) {
        return limetype === 'coworker' ? 'school_director' : 'guest_male';
    }
    isDisabled() {
        return !this.recipient.email && !this.recipient.mobile
            ? 'disabled'
            : '';
    }
    static get is() { return "recipient-item"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["recipient-item.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["recipient-item.css"]
        };
    }
    static get properties() {
        return {
            "recipient": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IRecipient",
                    "resolved": "IRecipient",
                    "references": {
                        "IRecipient": {
                            "location": "import",
                            "path": "../../types/Recipient",
                            "id": "src/types/Recipient.ts::IRecipient"
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
            "showAdd": {
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
                "attribute": "show-add",
                "reflect": false,
                "defaultValue": "true"
            }
        };
    }
}
//# sourceMappingURL=recipient-item.js.map
