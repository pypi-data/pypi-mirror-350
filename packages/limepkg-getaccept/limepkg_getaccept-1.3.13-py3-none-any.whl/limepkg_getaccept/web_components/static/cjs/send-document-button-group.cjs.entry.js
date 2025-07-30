'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const sendDocumentButtonGroupCss = ".send-document-button-group{margin-top:0.5rem}.send-document-button-group .send-document-button-open-in-ga{margin-left:0.5rem}limel-button{--lime-primary-color:#f49132}";
const SendDocumentButtonGroupStyle0 = sendDocumentButtonGroupCss;

const SendDocumentButtonGroup = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.validateDocument = index.createEvent(this, "validateDocument", 7);
        this.disabled = false;
        this.loading = false;
        this.handleOnClickSendButton = this.handleOnClickSendButton.bind(this);
    }
    render() {
        return [
            index.h("div", { key: 'c7c1a237f7c2035d9dffd56ea1818844ed8c1aee', class: "send-document-button-group" }, index.h("limel-button", { key: '673a56beed71d2a9d6b3e63f028071a0bdfe9119', label: "Prepare for sendout", primary: true, loading: this.loading, disabled: this.disabled, onClick: this.handleOnClickSendButton })),
        ];
    }
    handleOnClickSendButton() {
        this.validateDocument.emit();
    }
};
SendDocumentButtonGroup.style = SendDocumentButtonGroupStyle0;

exports.send_document_button_group = SendDocumentButtonGroup;

//# sourceMappingURL=send-document-button-group.cjs.entry.js.map