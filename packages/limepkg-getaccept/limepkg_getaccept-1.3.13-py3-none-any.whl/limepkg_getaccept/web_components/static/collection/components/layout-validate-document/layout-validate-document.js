/* eslint-disable camelcase */
/* eslint-disable sonarjs/no-identical-functions */
import { h } from "@stencil/core";
import { createDocument, fetchDocumentDetails, sealDocument, uploadDocument, } from "../../services";
import { EnumViews } from "../../models/EnumViews";
export class LayoutValidateDocument {
    constructor() {
        this.document = undefined;
        this.template = undefined;
        this.templateRoles = undefined;
        this.limeDocument = undefined;
        this.fields = undefined;
        this.platform = undefined;
        this.session = undefined;
        this.isSealed = false;
        this.isSending = undefined;
        this.isLoading = true;
        this.recipients = [];
        this.errorList = [];
        this.sentDocument = undefined;
        this.intervalId = undefined;
        this.handleCreateDocument = this.handleCreateDocument.bind(this);
        this.sealDocument = this.sealDocument.bind(this);
        this.hasProperty = this.hasProperty.bind(this);
        this.openInNewTab = this.openInNewTab.bind(this);
        this.handleOpenGetAccept = this.handleOpenGetAccept.bind(this);
    }
    async componentWillLoad() {
        await this.validateDocument();
    }
    render() {
        return (h("div", { key: '23189e82a7caf753c3db5853e0ef81919b33173a' }, (() => {
            if (this.isLoading) {
                return (h("ga-loader-with-text", { showText: this.isSending, text: "We are creating your document!" }));
            }
            else if (this.isSealed) {
                if (this.recipients.length > 0) {
                    return (h("div", { class: "share-document-container" }, h("h3", null, "Share document link:"), h("ul", { class: "share-document-recipient-list" }, this.recipients.map(recipient => {
                        return (h("share-document-link", { recipient: recipient }));
                    })), h("div", { class: "action-buttons" }, h("limel-button", { label: "Done", primary: true, onClick: () => {
                            this.documentCompleted.emit(false);
                        } }), h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }))));
                }
            }
            else {
                return (h("div", null, (() => {
                    if (this.errorList.length > 0) {
                        return (h("document-error-feedback", { document: this.document, errorList: this.errorList }));
                    }
                    else {
                        return (h("document-validate-info", { document: this.document }));
                    }
                })(), h("div", { class: "validate-document-button-container" }, (() => {
                    if (this.errorList.length === 0) {
                        return [
                            h("limel-button", { class: "send-button", label: "Send", primary: true, onClick: () => this.handleCreateDocument(true, false) }),
                            h("limel-button", { label: "Share document link", primary: false, onClick: () => this.handleCreateDocument(false, false) }),
                            h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }),
                        ];
                    }
                    else {
                        return (h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }));
                    }
                })())));
            }
        })()));
    }
    async handleUploadDocument() {
        if (this.limeDocument) {
            const { data, success } = await uploadDocument(this.platform, this.session, this.limeDocument.value);
            if (success) {
                return data.file_id;
            }
            else {
                this.errorHandler.emit('Could not upload Lime document to GetAccept');
            }
        }
        return '';
    }
    async handleCreateDocument(send, openDocument) {
        this.toggleLoading(true);
        const file_ids = await this.handleUploadDocument();
        const documentData = Object.assign(Object.assign({}, this.document), { template_id: this.template ? this.template.value : '', custom_fields: this.template ? this.fields : [], file_ids: file_ids, is_automatic_sending: send });
        const { data, success } = await createDocument(this.platform, this.session, documentData);
        if (!success) {
            this.errorHandler.emit('Could not create document. Make sure that all data is correctly supplied');
            this.toggleLoading(false);
            return;
        }
        if (openDocument) {
            this.intervalId = setInterval(() => this.openInGetacceptIfDraft(data, send, openDocument), 
            // eslint-disable-next-line @typescript-eslint/no-magic-numbers
            3000);
        }
        else {
            this.setDocumentData(data, send, openDocument);
        }
    }
    setDocumentData(data, send, openDocument) {
        this.sentDocument = Object.assign({}, data);
        if (!send && !openDocument) {
            this.sealDocument(data.id);
        }
        else {
            this.toggleLoading(false);
            this.documentCompleted.emit(false);
        }
    }
    async sealDocument(documentId, attempt = 1) {
        const maxAttempts = 5;
        const timeout = 5000;
        const { data, success } = await sealDocument(this.platform, this.session, documentId);
        if (!success && attempt < maxAttempts) {
            return setTimeout(() => this.sealDocument(documentId, (attempt += 1)), timeout);
        }
        else if (!success && attempt >= maxAttempts) {
            this.errorHandler.emit('Could not seal document do to lengthy import. Try to open it in GetAccept and seal it from there.');
            this.toggleLoading(false);
            return;
        }
        this.toggleLoading(false);
        this.recipients = data.recipients.map(recipient => {
            return {
                name: recipient.fullname,
                document_url: recipient.document_url,
                role: recipient.role,
                email: recipient.email,
            };
        });
        this.documentCompleted.emit(true);
    }
    handleOpenGetAccept() {
        if (this.sentDocument) {
            const openUrl = `https://app.getaccept.com/document/view/${this.sentDocument.id}`;
            this.openInNewTab(openUrl);
        }
    }
    async openInGetacceptIfDraft(data, send, openDocument) {
        const documentsDetails = await fetchDocumentDetails(this.platform, this.session, data.id);
        if (documentsDetails.status === 'draft') {
            const openUrl = `https://app.getaccept.com/document/edit/${data.id}`;
            this.openInNewTab(openUrl);
            this.setDocumentData(data, send, openDocument);
            clearInterval(this.intervalId);
        }
    }
    async validateDocument() {
        this.isLoading = true;
        if (!this.limeDocument && !this.template) {
            this.errorList.push({
                header: 'No document',
                title: 'You are missing a document.',
                icon: 'dog_tag',
                view: EnumViews.selectFile,
            });
        }
        if (this.document.recipients.length === 0) {
            this.errorList.push({
                header: 'No recipients',
                title: 'You need to add at least one recipient.',
                icon: 'user_male_circle',
                view: EnumViews.recipient,
            });
        }
        if (this.document.recipients.length > 0 &&
            this.document.is_signing &&
            !this.haveSigner()) {
            this.errorList.push({
                header: 'No signer',
                title: 'You need to add at least one signer when you are sending a documet for signing.',
                icon: 'autograph',
                view: EnumViews.recipient,
            });
        }
        if (this.haveNoTemplateRolesAdded()) {
            this.errorList.push({
                header: 'No template roles added.',
                title: 'You need to add all template roles.',
                icon: 'user_group_man_woman',
                view: EnumViews.templateRoles,
            });
        }
        if (this.document.recipients.length > 0 &&
            !this.document.is_sms_sending &&
            this.recipientsWithOnlyPhoneExists()) {
            this.errorList.push({
                header: 'Need to activate SMS sending',
                title: 'You need to activate SMS sendings due to recipients without email',
                icon: 'cell_phone',
                view: EnumViews.sendDocument,
            });
        }
        if (this.document.recipients.length > 0 &&
            this.recipientMissingEmailAndPhoneExists()) {
            this.errorList.push({
                header: 'Recipient missing contact information',
                title: 'One or many recipients are missing contact information',
                icon: 'about_us_male',
                view: EnumViews.recipient,
            });
        }
        this.isLoading = false;
    }
    haveSigner() {
        const signers = this.document.recipients.filter(recipient => recipient.role === 'signer');
        return signers.length > 0;
    }
    haveNoTemplateRolesAdded() {
        return (this.templateRoles &&
            this.templateRoles
                .filter(role => !(role.first_name || role.last_name || role.email))
                .some(role => !this.document.recipients.find(recipient => role.role_id === recipient.role_id)));
    }
    recipientsWithOnlyPhoneExists() {
        return this.document.recipients.some(recipient => !recipient.email && recipient.mobile !== '');
    }
    recipientMissingEmailAndPhoneExists() {
        return this.document.recipients.some(recipient => !recipient.email && !recipient.mobile);
    }
    hasProperty(value) {
        return value ? 'Yes' : 'No';
    }
    openInNewTab(url) {
        this.toggleLoading(false);
        this.documentCompleted.emit();
        if (url) {
            window.open(url, '_blank');
        }
    }
    toggleLoading(value) {
        this.isLoading = value;
        this.isSendingDocument.emit(value);
    }
    static get is() { return "layout-validate-document"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-validate-document.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-validate-document.css"]
        };
    }
    static get properties() {
        return {
            "document": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IDocument",
                    "resolved": "IDocument",
                    "references": {
                        "IDocument": {
                            "location": "import",
                            "path": "../../types/Document",
                            "id": "src/types/Document.ts::IDocument"
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
            "template": {
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
            "templateRoles": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "ITemplateRole[]",
                    "resolved": "ITemplateRole[]",
                    "references": {
                        "ITemplateRole": {
                            "location": "import",
                            "path": "src/types/TemplateRole",
                            "id": "src/types/TemplateRole.ts::ITemplateRole"
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
            "limeDocument": {
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
            "fields": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "ICustomField[]",
                    "resolved": "ICustomField[]",
                    "references": {
                        "ICustomField": {
                            "location": "import",
                            "path": "../../types/CustomField",
                            "id": "src/types/CustomField.ts::ICustomField"
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
            "platform": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "LimeWebComponentPlatform",
                    "resolved": "LimeWebComponentPlatform",
                    "references": {
                        "LimeWebComponentPlatform": {
                            "location": "import",
                            "path": "@limetech/lime-web-components",
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
            "session": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "ISession",
                    "resolved": "ISession",
                    "references": {
                        "ISession": {
                            "location": "import",
                            "path": "../../types/Session",
                            "id": "src/types/Session.ts::ISession"
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
            "isSealed": {
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
                "attribute": "is-sealed",
                "reflect": false,
                "defaultValue": "false"
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
            "isLoading": {},
            "recipients": {},
            "errorList": {},
            "sentDocument": {},
            "intervalId": {}
        };
    }
    static get events() {
        return [{
                "method": "documentCompleted",
                "name": "documentCompleted",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "boolean",
                    "resolved": "boolean",
                    "references": {}
                }
            }, {
                "method": "errorHandler",
                "name": "errorHandler",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "string",
                    "resolved": "string",
                    "references": {}
                }
            }, {
                "method": "isSendingDocument",
                "name": "isSendingDocument",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "boolean",
                    "resolved": "boolean",
                    "references": {}
                }
            }];
    }
}
//# sourceMappingURL=layout-validate-document.js.map
