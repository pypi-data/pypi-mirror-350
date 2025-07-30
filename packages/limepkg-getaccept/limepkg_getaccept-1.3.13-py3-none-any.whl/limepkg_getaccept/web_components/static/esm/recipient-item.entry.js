import { r as registerInstance, h } from './index-0b1d787f.js';

const recipientItemCss = ".recipient-list-item{display:flex;align-items:center;padding:0.5rem;cursor:pointer;overflow:hidden;border-bottom:1px solid #ccc}.recipient-list-item:hover{background-color:rgb(var(--contrast-300))}.recipient-list-item.disabled{opacity:0.7;filter:grayscale(1);-webkit-filter:grayscale(1)}.recipient-list-item .recipient-icon{display:flex;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1;color:#fff}.recipient-list-item .recipient-icon.coworker{background-color:#f49132}.recipient-list-item .recipient-info-container{display:flex;flex-direction:column;font-size:0.7rem;flex-grow:2}.recipient-list-item .recipient-info-container .recipient-info-contact-data{display:flex;flex-wrap:wrap;overflow:hidden}.recipient-list-item .recipient-info-container .recipient-info-contact-data .recipient-phone:empty{display:none}.recipient-list-item .recipient-info-container .recipient-info-contact-data.contact--email .recipient-phone::before{content:\"|\";margin:0 0.5rem}.recipient-list-item .recipient-add-button{color:#f49132}";
const RecipientItemStyle0 = recipientItemCss;

const RecipientItem = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
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
};
RecipientItem.style = RecipientItemStyle0;

export { RecipientItem as recipient_item };

//# sourceMappingURL=recipient-item.entry.js.map