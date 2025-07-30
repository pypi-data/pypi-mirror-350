'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const recipientItemAddedCss = ".recipient-list-item{display:flex;align-items:center;padding:0.5rem;cursor:pointer;border-bottom:1px solid #ccc}.recipient-list-item:hover{background-color:rgb(var(--contrast-300))}.recipient-list-item .recipient-icon{display:flex;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1}.recipient-list-item .recipient-info-container{display:flex;flex-direction:column;flex-grow:2;font-size:0.7rem}.recipient-list-item .recipient-info-container .recipient-info-contact-data{display:flex;flex-wrap:wrap;overflow:hidden}.recipient-list-item .recipient-role-container{padding:0.5rem 1rem}.recipient-list-item .recipient-role-container .recipient-role-list{padding:0.5rem;border:none;background-color:transparent;outline:none;color:#212121}.recipient-list-item .recipient-remove-button{display:flex;color:#f88987}";
const RecipientItemAddedStyle0 = recipientItemAddedCss;

const RecipientItemAdded = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeRecipientRole = index.createEvent(this, "changeRecipientRole", 7);
        this.removeRecipient = index.createEvent(this, "removeRecipient", 7);
        this.roles = [];
        this.recipient = undefined;
        this.isSigning = undefined;
        this.handleChangeRole = this.handleChangeRole.bind(this);
        this.handleRemoveRecipient = this.handleRemoveRecipient.bind(this);
        this.selectedRole = this.selectedRole.bind(this);
    }
    componentWillLoad() {
        this.addRecipientRoles();
    }
    addRecipientRoles() {
        if (this.isSigning) {
            this.roles.push({
                value: 'signer',
                label: 'Signer',
            });
        }
        this.roles.push({
            value: 'cc',
            label: 'Viewer',
        }, {
            value: 'approver',
            label: 'Internal approver',
        }, {
            value: 'externalApprover',
            label: 'External approver',
        });
        if (!this.recipient.role) {
            this.recipient.role = this.roles[0].value;
            this.changeRecipientRole.emit(this.recipient);
        }
    }
    render() {
        const { fullname, email } = this.recipient;
        return (index.h("li", { key: '1de674ef777018a7ae86b1279c93222224a69286', class: "recipient-list-item" }, index.h("div", { key: 'ec2a82dab4008a9fc571d0cff673e9f4c165f4ae', class: "recipient-info-container" }, index.h("span", { key: 'bdb5317ddd3a284fdd75bc1807763a2dc4ade722' }, fullname), index.h("div", { key: 'f3104fdc1db174741fa1ede7b73480cf16bc9094', class: "recipient-info-contact-data" }, index.h("span", { key: '55a5d96b0704141b3fc162e3897204e0326c4a39' }, email))), index.h("div", { key: '15933045922782ebbaea98037d6af9626bbfa819', class: "recipient-role-container" }, index.h("select", { key: '59b33bd5388f4a30a157194c2740ff8912723c48', class: "recipient-role-list", onInput: event => this.handleChangeRole(event) }, this.roles.map(role => {
            return (index.h("option", { value: role.value, selected: this.selectedRole(role) }, role.label));
        }))), index.h("div", { key: '8a3630597d871e2f86ca3ba005fde755ff86deca', class: "recipient-remove-button", onClick: this.handleRemoveRecipient }, index.h("limel-icon", { key: '16e521d9329db35be7957bbafc241a3c31e456aa', name: "trash", size: "small" }))));
    }
    handleChangeRole(event) {
        this.recipient.role = event.target.value;
        this.changeRecipientRole.emit(this.recipient);
    }
    handleRemoveRecipient() {
        this.removeRecipient.emit(this.recipient);
    }
    selectedRole(role) {
        return this.recipient.role === role.value;
    }
};
RecipientItemAdded.style = RecipientItemAddedStyle0;

const selectedRecipientListCss = ".recipient-list{list-style-type:none;padding:0;margin:0}";
const SelectedRecipientListStyle0 = selectedRecipientListCss;

const SelectedRecipientList = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.recipients = undefined;
        this.document = undefined;
    }
    render() {
        if (!this.recipients.length) {
            return (index.h("empty-state", { icon: "user", text: "No recipients added. Find and add recipients to the left!" }));
        }
        return (index.h("ul", { class: "recipient-list" }, this.recipients.map(selectedRecipient => {
            return (index.h("recipient-item-added", { recipient: selectedRecipient, isSigning: this.document.is_signing }));
        })));
    }
};
SelectedRecipientList.style = SelectedRecipientListStyle0;

exports.recipient_item_added = RecipientItemAdded;
exports.selected_recipient_list = SelectedRecipientList;

//# sourceMappingURL=recipient-item-added_2.cjs.entry.js.map