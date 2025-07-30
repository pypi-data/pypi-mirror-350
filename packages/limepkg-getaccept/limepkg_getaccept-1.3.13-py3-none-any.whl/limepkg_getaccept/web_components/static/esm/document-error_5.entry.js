import { r as registerInstance, c as createEvent, h } from './index-0b1d787f.js';

const documentErrorCss = ".document-error{display:flex;align-items:center;padding:1rem 1rem;cursor:pointer}.document-error .document-error-icon{display:inherit;padding:0.5rem;margin-right:1.5rem;border-radius:50%;background-color:#f88987;color:#fff}.document-error .document-error-info{display:flex;flex-direction:column}.document-error .document-error-info .document-error-header{margin-block-end:0;margin-block-start:0}.document-error:hover{background-color:#f5f5f5}@media (min-width: 1074px){.document-error{width:50%}}@media (max-width: 1075px){.document-error{width:100%}}";
const DocumentErrorStyle0 = documentErrorCss;

const DocumentError = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
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
};
DocumentError.style = DocumentErrorStyle0;

const documentErrorFeedbackCss = ".document-error-list{padding:0}";
const DocumentErrorFeedbackStyle0 = documentErrorFeedbackCss;

const DocumentErrorFeedback = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.document = undefined;
        this.errorList = [];
    }
    render() {
        return [
            h("div", { key: '6518d28dabf6d7de6e4fd21ff5d86d187f437085' }, h("h3", { key: '08887413747c6a5ee7ea2cf91c5d03726d0c5020' }, "You need to fix following tasks to send:"), h("ul", { key: '3b81a34f6f1cac3e6984b601ce46b74382f2f421', class: "document-error-list" }, this.errorList.map(error => {
                return h("document-error", { error: error });
            }))),
        ];
    }
};
DocumentErrorFeedback.style = DocumentErrorFeedbackStyle0;

const documentValidateInfoCss = ".validate-document-success{display:flex;flex-wrap:wrap}@media (min-width: 768px){.validate-document-success .validate-document-summary{width:50%}.validate-document-success .validate-document-recipients{width:50%}}@media (max-width: 769px){.validate-document-success .validate-document-summary{width:100%}.validate-document-success .validate-document-recipients{width:100%}}.validate-document-success .validate-document-property-list{list-style-type:none;margin:0;padding:0rem;width:100%}.validate-document-success .validate-document-property-list .document-property{font-weight:bold}.validate-document-success .document-recipient-list{margin:0 0 1rem 0;width:100%;padding:0rem}limel-button{--lime-primary-color:#f49132}";
const DocumentValidateInfoStyle0 = documentValidateInfoCss;

const DocumentValidateInfo = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.document = undefined;
        this.hasProperty = this.hasProperty.bind(this);
    }
    render() {
        return [
            h("div", { key: 'eab3018e946c0b877de52b8ccd98060e2aafb9b3', class: "validate-document-success" }, h("div", { key: 'b777252d4ee8297aede9236783072d306abeab3a', class: "validate-document-summary" }, h("h3", { key: '2f8cea556c35a909763e32a1b7317f305053b460' }, "Summary"), h("ul", { key: 'dc5409bad2247f940d01625f5e2a8f00600e1db8', class: "validate-document-property-list" }, h("li", { key: '0ab733745b1879f9b1e27c62bcbad794c33c0b02' }, h("span", { key: 'f29129b9d835ac1ffec0fef1ec4ec11c197ca2bd', class: "document-property" }, "Name: "), h("span", { key: 'edb4567263bb951acb5c9501179569c779fa0235' }, this.document.name)), h("li", { key: '8e84e239f33de4769ea42e7983279f02d4e30bb0' }, h("span", { key: '26cd9b0134321215534693cfd98e007ce11634cd', class: "document-property" }, "Value: "), h("span", { key: '9ea4540f89ae22b3dc2cd1759e581c79451e1776' }, this.document.value)), h("li", { key: 'bdf45b7246c1a51af287a1e39192a9f17b37be5e' }, h("span", { key: '67bb8405cd8ac1f8336ec846d47b3ef8a811b910', class: "document-property" }, "Document is for signing:", ' '), h("span", { key: '30f47ba2c6bf822ac183a56408ccb24ce4449eec' }, this.hasProperty(this.document.is_signing))), h("li", { key: 'cdd406b3b78c9249e54dc436761c8e6683b8eb4c' }, h("span", { key: 'b2ba4f0eb910b87c29e142dcf53c7197759385e1', class: "document-property" }, "Video is added:", ' '), h("span", { key: '66316de5bc227fe9497c212d143c981187b77652' }, this.hasProperty(this.document.is_video))), h("li", { key: 'dcd93780bb43f363f47165427614ecf1a9434510' }, h("span", { key: '7c59b9066b1527c15cdeb7854d294487cfcbdb88', class: "document-property" }, "Send smart reminders:", ' '), h("span", { key: 'feaa4ace7b819750f00e269e59c77d98281cfe32' }, this.hasProperty(this.document.is_reminder_sending))), h("li", { key: 'f78060dff948e73691a71b09f236fb5949eab3f2' }, h("span", { key: 'ea0f58fd634f82edf3bb6a0aa230140d51ff5d81', class: "document-property" }, "Send link by SMS:", ' '), h("span", { key: '3b7a21427359bed62fe31d617e11557c7b7e0a96' }, this.hasProperty(this.document.is_sms_sending))))), h("div", { key: 'fc6f685ada3568f7b79d56c693e3c798480bc931', class: "validate-document-recipients" }, h("h3", { key: '482bc0d7acc6e099c95b891123a838c33fd262bd' }, "Recipients"), h("ul", { key: '6f073fab924fc49aa29ff3055210ccbb38288034', class: "document-recipient-list" }, this.document.recipients.map(recipient => {
                return (h("recipient-item", { recipient: recipient, showAdd: false }));
            })))),
        ];
    }
    hasProperty(value) {
        return value ? 'Yes' : 'No';
    }
};
DocumentValidateInfo.style = DocumentValidateInfoStyle0;

const gaLoaderWithTextCss = "limel-spinner{margin:2rem 0;color:#f49132}.share-document-loading-container{text-align:center;margin-top:3rem}";
const GaLoaderWithTextStyle0 = gaLoaderWithTextCss;

const GALoaderWithText = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
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
};
GALoaderWithText.style = GaLoaderWithTextStyle0;

const shareDocumentLinkCss = ".share-document-list-item{margin:0.5rem 0;padding:0.5rem 1rem}.share-document-list-item .recipient-info-container{display:flex;align-items:center;padding-left:1rem}.share-document-list-item .recipient-info-container .recipient-icon{display:flex;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1;color:#fff}.share-document-list-item .recipient-info-container .recipient-info{display:flex;flex-direction:column}.share-document-list-item .recipient-info-container .recipient-info .recipient-info-name{text-transform:capitalize;font-weight:bold}.share-document-list-item .recipient-info-container .recipient-info .recipient-info{text-transform:capitalize}";
const ShareDocumentLinkStyle0 = shareDocumentLinkCss;

const ShareDocumentLink = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.recipient = undefined;
        this.handleCopyLink = this.handleCopyLink.bind(this);
    }
    render() {
        return (h("li", { key: '262815491c2a7ae7c2311acbb76e81335efa64fc', class: "share-document-list-item" }, h("div", { key: '64422961902488b16f6350ef39f69ba4a6923dee', class: "recipient-info-container" }, h("div", { key: '4169a8781fd0f2231ddcf5907a699cbbb2ab3757', class: "recipient-icon" }, h("limel-icon", { key: '6401d83e3a3efe3419eabce499cb4c55ae881b2d', name: "user", size: "small" })), h("div", { key: '9ba77fa755a0545b043972499ef1d70e9ea8a546', class: "recipient-info" }, h("span", { key: '9fc87e43ba13ee561e74bceb516d751308a86342', class: "recipient-info-name" }, this.recipient.fullname), h("span", { key: '4d59419a455516a99753c046108e849637e1f4eb', class: "recipient-info-role" }, this.recipient.role))), h("div", { key: '3920f52319f0ce4770b49a49cdf2080b82df0cdd' }, h("limel-input-field", { key: '3e2befb3a12d33f247edd483abe321d0e5ace93c', label: "Signing link", type: "email", value: this.recipient.document_url, trailingIcon: "copy_link", onAction: this.handleCopyLink }))));
    }
    handleCopyLink() {
        const copyText = document.createElement('textarea');
        copyText.value = this.recipient.document_url;
        document.body.appendChild(copyText);
        copyText.select();
        document.execCommand('copy');
        document.body.removeChild(copyText);
    }
};
ShareDocumentLink.style = ShareDocumentLinkStyle0;

export { DocumentError as document_error, DocumentErrorFeedback as document_error_feedback, DocumentValidateInfo as document_validate_info, GALoaderWithText as ga_loader_with_text, ShareDocumentLink as share_document_link };

//# sourceMappingURL=document-error_5.entry.js.map