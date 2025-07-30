import { r as registerInstance, c as createEvent, h, g as getElement } from './index-0b1d787f.js';
import { E as EnumViews } from './EnumViews-b32e9b99.js';
import { f as fetchMe, a as fetchEntity, b as fetchSentDocuments, r as refreshToken } from './index-fd1933d7.js';
import { w as workflowSteps } from './workflow-steps-ef1ed8f2.js';

const lwcGetacceptRootCss = "limel-dialog{--dialog-heading-icon-background-color:#f49132}limel-dialog.preview-view{--dialog-width:35rem;--dialog-height:45rem}limel-dialog.aside{--dialog-width:34rem}limel-dialog .ga-version{position:absolute;top:0;right:50px}limel-dialog .ga-body{overflow:auto;min-height:100%;margin-top:1rem}limel-dialog .ga-top-bar{position:sticky;top:0;height:5rem;background-color:rgb(var(--contrast-100));z-index:4;display:flex;align-items:center;z-index:9}@media (min-width: 1074px){limel-dialog{--dialog-width:65rem;--dialog-height:40rem}}@media (max-width: 1075px){limel-dialog{--dialog-width:55rem;--dialog-height:40rem}}@media (min-width: 1800px){limel-dialog{--dialog-width:70rem;--dialog-height:60rem}}limel-button{--lime-primary-color:#f49132}.logo-container{height:2.2rem;width:15rem;margin-bottom:1rem;cursor:pointer;transition:width 0.5s;overflow:hidden}.logo-container.compact{width:2.5rem}.logo-container:hover{opacity:0.8}.logo-container .logo{height:2.2rem}.close{display:block;position:absolute;right:-1rem;top:0rem;cursor:pointer}.close:hover{color:#eee}.actionpad-container{width:100%}.getaccept-button{width:100%;display:flex;justify-content:start;align-items:center;padding:0.425rem 0.875rem 0.425rem 0.875rem;border:none;border-radius:2rem;cursor:pointer;transition:background 0.8s;background-position:center;font-size:0.8rem;font-weight:bold;color:#444;background:#eee}.getaccept-button:focus{outline:0}.getaccept-button:hover{background:#f5f5f5 radial-gradient(circle, transparent 1%, #f5f5f5 1%) center/15000%}.getaccept-button:active{background-color:white;background-size:100%;transition:background 0s}.getaccept-button img{height:2rem;flex:0}.getaccept-button .button-text{margin-left:0.5rem;flex:2;text-align:left}.getaccept-button .document-count{margin-left:auto;display:flex;align-items:center}.getaccept-button .document-count limel-icon{margin-right:0.3rem}workflow-progress-bar{position:absolute;top:1.5rem;left:4rem;right:4rem}";
const LwcGetacceptRootStyle0 = lwcGetacceptRootCss;

const Root = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.errorHandler = createEvent(this, "errorHandler", 7);
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
    get element() { return getElement(this); }
};
Root.style = LwcGetacceptRootStyle0;

export { Root as lwc_getaccept_root };

//# sourceMappingURL=lwc-getaccept-root.entry.js.map