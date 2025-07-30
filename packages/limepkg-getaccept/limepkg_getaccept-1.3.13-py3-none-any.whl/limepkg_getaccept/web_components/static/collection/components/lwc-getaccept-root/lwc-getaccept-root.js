import { h, } from "@stencil/core";
import { EnumViews } from "../../models/EnumViews";
import { fetchMe, fetchEntity, refreshToken, fetchSentDocuments, } from "../../services";
import { workflowSteps } from "../workflow-progress-bar/workflow-steps";
export class Root {
    constructor() {
        this.platform = undefined;
        this.context = undefined;
        this.company = undefined;
        this.externalId = undefined;
        this.isOpen = false;
        this.session = undefined;
        this.user = undefined;
        this.entities = [];
        this.documentId = undefined;
        this.activeView = EnumViews.login;
        this.documentData = undefined;
        this.isSealed = undefined;
        this.template = undefined;
        this.limeDocument = undefined;
        this.templateFields = undefined;
        this.templateRoles = undefined;
        this.errorMessage = '';
        this.documents = [];
        this.isLoadingDocuments = undefined;
        this.isSending = false;
        this.openDialog = this.openDialog.bind(this);
        this.handleLogoClick = this.handleLogoClick.bind(this);
        this.renderLayout = this.renderLayout.bind(this);
        this.loadInitialData = this.loadInitialData.bind(this);
        this.loadSentDocuments = this.loadSentDocuments.bind(this);
        this.showWorkflow = this.showWorkflow.bind(this);
    }
    componentWillLoad() {
        this.externalId = `${this.context.limetype}_${this.context.id}`;
        this.activeView = this.checkIfSessionExists
            ? EnumViews.home
            : EnumViews.login;
        if (this.session) {
            this.loadInitialData();
        }
        this.setDefaultDocumentData();
    }
    async loadInitialData() {
        this.loadSentDocuments();
        try {
            const { user, entities } = await fetchMe(this.platform, this.session);
            this.user = user;
            this.entities = entities;
        }
        catch (e) {
            this.errorHandler.emit('Could not load user session. Try relogging');
        }
        this.loadEntityDetails();
    }
    async loadEntityDetails() {
        try {
            const { entity } = await fetchEntity(this.platform, this.session);
            this.session.entity_id = entity.id;
            this.documentData.email_send_message =
                entity.email_send_message !== ''
                    ? entity.email_send_message
                    : entity.default_email_send_message;
            this.documentData.email_send_subject =
                entity.email_send_subject !== ''
                    ? entity.email_send_subject
                    : entity.default_email_send_subject;
        }
        catch (e) {
            this.errorHandler.emit('Could not load user session. Try relogging');
        }
    }
    render() {
        return [
            h("limel-flex-container", { key: 'fbeb6317b6240426b71f28d92e65c463234d18e5', class: "actionpad-container" }, h("button", { key: '803aa1e17fb61f4d1a5110d41aa8122069e7d622', class: "getaccept-button", onClick: this.openDialog }, h("img", { key: '3d5cd8e96f36e574d4e43c640c7268f7ce8c350b', src: "https://static-vue-rc.getaccept.com/img/integrations/logo_only.png" }), h("span", { key: '03cb3179518ca8ddeae70ffa2c7503698fea5cf2', class: "button-text" }, "Send document"), this.renderDocumentCount(!!this.session))),
            h("limel-dialog", { key: '1c9838054bd8cb206070a52e7b9738710f8bae1d', open: this.isOpen, closingActions: { escapeKey: true, scrimClick: false }, onClose: () => {
                    this.isOpen = false;
                }, class: { aside: this.checkIsAside() } }, h("div", { key: '287204612d9e1011ebd778fcdbc5ccb38886344c', class: "ga-top-bar" }, this.renderLogo(this.showWorkflow()), h("limel-icon", { key: '4be4bc4dbeb583b1845bae71aa699afa28016ded', class: "close", name: "cancel", size: "small", onClick: () => {
                    this.isOpen = false;
                } }), (() => {
                if (this.activeView !== EnumViews.login) {
                    return [
                        h("layout-menu", { activeView: this.activeView, isSending: this.isSending }),
                        h("workflow-progress-bar", { isVisible: this.showWorkflow(), activeView: this.activeView }),
                    ];
                }
            })()), h("div", { key: 'd3cd2c6dee77432ded9b2d228518a8df4bd553bf', class: "ga-body" }, this.renderLayout()), h("div", { key: '92baf0e4e5394361ad2e9c38bbcc80897f6771f3', class: "ga-version" }, h("span", { key: '8d00157e0e0a8a42e54a69780a8f8250f5be3e24' }, "Version: 1.3.13")), h("limel-button-group", { key: 'f10868e722a00d6a31f410e64966ea8fbd0e28b4', slot: "button" }, h("limel-button", { key: 'b28504cdcc8f8db75a5a8b85d246a62f4bc5c5ce', label: "Cancel", onClick: () => {
                    this.isOpen = false;
                } })), h("error-message", { key: 'e4ca6f8b2d0e6162fd2768cd7dccd96068c7f7f8', error: this.errorMessage })),
        ];
    }
    checkIsAside() {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m;
        return (((_m = (_l = (_k = (_j = (_h = (_g = (_f = (_e = (_d = (_c = (_b = (_a = this.element.parentNode) === null || _a === void 0 ? void 0 : _a.parentNode) === null || _b === void 0 ? void 0 : _b.parentNode) === null || _c === void 0 ? void 0 : _c.parentNode) === null || _d === void 0 ? void 0 : _d.host) === null || _e === void 0 ? void 0 : _e.parentNode) === null || _f === void 0 ? void 0 : _f.parentNode) === null || _g === void 0 ? void 0 : _g.host) === null || _h === void 0 ? void 0 : _h.parentNode) === null || _j === void 0 ? void 0 : _j.parentNode) === null || _k === void 0 ? void 0 : _k.host) === null || _l === void 0 ? void 0 : _l.parentNode) === null || _m === void 0 ? void 0 : _m.tagName) === 'ASIDE');
    }
    renderDocumentCount(hasSession) {
        if (hasSession) {
            return (h("span", { class: "document-count" }, h("limel-icon", { name: "file", size: "small" }), h("span", null, this.documents.length)));
        }
        return [];
    }
    renderLogo(compact) {
        const classes = `logo-container ${compact ? 'compact' : ''}`;
        return (h("div", { class: classes }, h("img", { onClick: this.handleLogoClick, src: "https://static-vue-rc.getaccept.com/img/integrations/logo-inverted.png", class: "logo" })));
    }
    showWorkflow() {
        if (this.isSending || this.isSealed) {
            return false;
        }
        return workflowSteps.some(view => view.currentView === this.activeView);
    }
    renderLayout() {
        switch (this.activeView) {
            case EnumViews.home:
                return (h("layout-overview", { platform: this.platform, session: this.session, externalId: this.externalId, documents: this.documents, isAside: this.checkIsAside() }));
            case EnumViews.login:
                return h("layout-login", { platform: this.platform });
            case EnumViews.selectFile:
                return (h("layout-select-file", { platform: this.platform, session: this.session, context: this.context, selectedLimeDocument: this.limeDocument, selectedTemplate: this.template, customFields: this.templateFields, templateRoles: this.templateRoles }));
            case EnumViews.templateRoles:
                return (h("layout-template-roles", { platform: this.platform, session: this.session, context: this.context, document: this.documentData, limeDocument: this.limeDocument, template: this.template, templateRoles: this.templateRoles }));
            case EnumViews.recipient:
                return (h("layout-select-recipient", { platform: this.platform, document: this.documentData, context: this.context, isAside: this.checkIsAside() }));
            case EnumViews.settings:
                return (h("layout-settings", { user: this.user, entities: this.entities, session: this.session, platform: this.platform }));
            case EnumViews.help:
                return h("layout-help", null);
            case EnumViews.sendDocument:
                return (h("layout-send-document", { context: this.context, document: this.documentData, limeDocument: this.limeDocument, template: this.template, session: this.session, platform: this.platform }));
            case EnumViews.videoLibrary:
                return (h("layout-video-library", { platform: this.platform, session: this.session }));
            case EnumViews.documentDetail:
                return (h("layout-document-details", { platform: this.platform, session: this.session, documentId: this.documentId }));
            case EnumViews.documentValidation:
                return (h("layout-validate-document", { platform: this.platform, session: this.session, document: this.documentData, limeDocument: this.limeDocument, template: this.template, fields: this.templateFields, isSealed: this.isSealed, isSending: this.isSending, templateRoles: this.templateRoles }));
            default:
                return h("layout-overview", null);
        }
    }
    logout() {
        localStorage.removeItem('getaccept_session');
        this.documents = [];
        this.activeView = EnumViews.login;
    }
    openDialog() {
        this.isOpen = true;
        if (this.checkIsPreviewView) {
            this.element.shadowRoot.lastElementChild.classList.add('preview-view');
        }
    }
    handleLogoClick() {
        this.activeView = this.checkIfSessionExists
            ? EnumViews.home
            : EnumViews.login;
    }
    async loadSentDocuments() {
        this.isLoadingDocuments = true;
        try {
            this.documents = await fetchSentDocuments(this.platform, this.externalId, this.session);
        }
        catch (e) {
            this.errorHandler.emit('Something went wrong while documents from GetAccept...');
        }
        this.isLoadingDocuments = false;
    }
    changeViewHandler(view) {
        if (view.detail === EnumViews.logout) {
            this.logout();
        }
        else if (this.isSealed) {
            this.activeView = EnumViews.home;
            this.setDefaultDocumentData();
        }
        else {
            this.activeView = view.detail;
        }
    }
    loadRealtedDocumentsHandler() {
        this.loadSentDocuments();
    }
    setTemplate(event) {
        this.template = event.detail;
        this.documentData.name = event.detail.text;
        this.limeDocument = null;
        this.templateFields = [];
    }
    setLimeDocument(event) {
        this.limeDocument = event.detail;
        this.documentData.name = event.detail.text;
        this.template = null;
        this.templateRoles = null;
        this.templateFields = [];
    }
    setCustomFields(event) {
        this.templateFields = event.detail;
    }
    setTemplateRoles(event) {
        this.templateRoles = event.detail;
        this.documentData = Object.assign(Object.assign({}, this.documentData), { recipients: this.documentData.recipients.map(recipient => (Object.assign(Object.assign({}, recipient), { role_id: '' }))) });
    }
    updateDocumentRecipientHandler(recipients) {
        this.documentData.recipients = recipients.detail;
    }
    documentTypeHandler(isSigning) {
        this.documentData.is_signing = isSigning.detail;
    }
    setSessionHandler(sessionData) {
        this.setSessionData(sessionData.detail);
        this.activeView = EnumViews.home;
        this.loadInitialData();
    }
    setDocumentName(documentName) {
        this.documentData = Object.assign(Object.assign({}, this.documentData), { name: documentName.detail });
    }
    setDocumentValue(value) {
        this.documentData = Object.assign(Object.assign({}, this.documentData), { value: value.detail });
    }
    setDocumentSmartReminder(smartReminder) {
        this.documentData.is_reminder_sending = smartReminder.detail;
    }
    setDocumentIsSmsSending(isSmsSending) {
        this.documentData.is_sms_sending = isSmsSending.detail;
    }
    setDocumentEmailSubject(emailSendSubject) {
        this.documentData.email_send_subject = emailSendSubject.detail;
    }
    setDocumentEmailMessage(emailSendMessage) {
        this.documentData.email_send_message = emailSendMessage.detail;
    }
    validateDocumentHandler() {
        this.activeView = EnumViews.documentValidation;
    }
    openDocumentDetails(document) {
        this.activeView = EnumViews.documentDetail;
        this.documentId = document.detail.id;
    }
    updateRecipientRole(event) {
        const newRecipients = [...this.documentData.recipients];
        const recipientIndex = newRecipients.findIndex(recipient => recipient.email === event.detail.recipient.email &&
            recipient.lime_id === event.detail.recipient.lime_id);
        newRecipients[recipientIndex].role_id = event.detail.role.role_id;
        this.documentData = Object.assign(Object.assign({}, this.documentData), { recipients: [...newRecipients] });
    }
    setDocumentVideo(videoId) {
        this.documentData.video_id = videoId.detail;
        this.documentData.is_video = true;
    }
    removeDocumentVideo() {
        this.documentData.video_id = '';
        this.documentData.is_video = false;
    }
    setIsSending(isSending) {
        this.isSending = isSending.detail;
    }
    documentCompleted(isSealed) {
        this.setDefaultDocumentData();
        this.loadEntityDetails();
        this.isSealed = isSealed.detail;
        if (!this.isSealed) {
            this.activeView = EnumViews.home;
        }
        this.loadSentDocuments();
    }
    onError(event) {
        this.errorMessage = event.detail;
        // eslint-disable-next-line @typescript-eslint/no-magic-numbers
        setTimeout(() => (this.errorMessage = ''), 100); // Needed for same consecutive error message
    }
    get checkIfSessionExists() {
        const storedSession = window.localStorage.getItem('getaccept_session');
        if (storedSession) {
            const sessionObj = JSON.parse(storedSession);
            // used to check if token should be refreshed or not.
            this.validateToken(sessionObj);
            this.session = sessionObj;
        }
        return !!storedSession;
    }
    get checkIsPreviewView() {
        return document
            .querySelector('lime-webclient')
            .shadowRoot.activeElement.classList.contains('has-side-panel-open');
    }
    async validateToken(session) {
        try {
            const { data, success } = await refreshToken(this.platform, session);
            if (success) {
                const storedSession = window.localStorage.getItem('getaccept_session');
                if (storedSession) {
                    const sessionObj = JSON.parse(storedSession);
                    sessionObj.expires_in = data.expires_in;
                    sessionObj.access_token = data.access_token;
                    this.setSessionData(sessionObj);
                }
            }
            else {
                this.errorMessage = 'Could not refresh token.';
                setTimeout(() => (this.errorMessage = ''));
            }
        }
        catch (error) {
            this.errorMessage = 'Could not refresh token.';
            setTimeout(() => (this.errorMessage = ''));
            this.logout();
        }
        return true;
    }
    setSessionData(session) {
        window.localStorage.setItem('getaccept_session', JSON.stringify(session));
        this.session = session;
    }
    setDefaultDocumentData() {
        this.documentData = {
            is_signing: false,
            name: '',
            recipients: [],
            template_id: '',
            custom_fields: [],
            is_reminder_sending: false,
            is_sms_sending: false,
            email_send_subject: '',
            email_send_message: '',
            video_id: '',
            is_video: false,
            external_id: this.externalId,
            value: 0,
        };
        this.templateFields = [];
        this.isSealed = false;
        this.template = null;
        this.limeDocument = null;
    }
    static get is() { return "lwc-getaccept-root"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["lwc-getaccept-root.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["lwc-getaccept-root.css"]
        };
    }
    static get properties() {
        return {
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
                    "text": "Reference to the platform"
                }
            },
            "context": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "LimeWebComponentContext",
                    "resolved": "LimeWebComponentContext",
                    "references": {
                        "LimeWebComponentContext": {
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
                    "text": "The context this component belongs to"
                }
            },
            "company": {
                "type": "any",
                "mutable": false,
                "complexType": {
                    "original": "any",
                    "resolved": "any",
                    "references": {}
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "company",
                "reflect": false
            }
        };
    }
    static get states() {
        return {
            "externalId": {},
            "isOpen": {},
            "session": {},
            "user": {},
            "entities": {},
            "documentId": {},
            "activeView": {},
            "documentData": {},
            "isSealed": {},
            "template": {},
            "limeDocument": {},
            "templateFields": {},
            "templateRoles": {},
            "errorMessage": {},
            "documents": {},
            "isLoadingDocuments": {},
            "isSending": {}
        };
    }
    static get events() {
        return [{
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
            }];
    }
    static get elementRef() { return "element"; }
    static get listeners() {
        return [{
                "name": "changeView",
                "method": "changeViewHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "loadRelatedDocuments",
                "method": "loadRealtedDocumentsHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setTemplate",
                "method": "setTemplate",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setLimeDocument",
                "method": "setLimeDocument",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setCustomFields",
                "method": "setCustomFields",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setTemplateRoles",
                "method": "setTemplateRoles",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "updateDocumentRecipient",
                "method": "updateDocumentRecipientHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setDocumentType",
                "method": "documentTypeHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setSession",
                "method": "setSessionHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setNewDocumentName",
                "method": "setDocumentName",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setDocumentValue",
                "method": "setDocumentValue",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setSmartReminder",
                "method": "setDocumentSmartReminder",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setIsSmsSending",
                "method": "setDocumentIsSmsSending",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setEmailSubject",
                "method": "setDocumentEmailSubject",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setEmailMessage",
                "method": "setDocumentEmailMessage",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "validateDocument",
                "method": "validateDocumentHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "openDocument",
                "method": "openDocumentDetails",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "recipientRoleUpdated",
                "method": "updateRecipientRole",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "setVideo",
                "method": "setDocumentVideo",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "removeVideo",
                "method": "removeDocumentVideo",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "isSendingDocument",
                "method": "setIsSending",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "documentCompleted",
                "method": "documentCompleted",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "errorHandler",
                "method": "onError",
                "target": undefined,
                "capture": false,
                "passive": false
            }];
    }
}
//# sourceMappingURL=lwc-getaccept-root.js.map
