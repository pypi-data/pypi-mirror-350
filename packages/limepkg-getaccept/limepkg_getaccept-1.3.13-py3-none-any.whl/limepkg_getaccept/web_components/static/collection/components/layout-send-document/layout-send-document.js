import { h } from "@stencil/core";
import { EnumViews } from "../../models/EnumViews";
import { fetchDealValue } from "../../services/index";
export class LayoutSendDocument {
    async componentWillLoad() {
        this.documentName = this.fileName();
        this.setNewDocumentName.emit(this.documentName);
        this.value = this.document.value || 0;
        this.smartReminder = this.document.is_reminder_sending;
        this.sendLinkBySms = this.document.is_sms_sending;
        this.documentVideo = this.document.video_id !== '';
        await this.loadObjectValue();
    }
    componentDidUpdate() {
        this.value = this.document.value;
        this.documentName = this.document.name || this.fileName();
    }
    constructor() {
        this.document = undefined;
        this.template = undefined;
        this.limeDocument = undefined;
        this.platform = undefined;
        this.session = undefined;
        this.context = undefined;
        this.documentName = '';
        this.value = 0;
        this.smartReminder = false;
        this.sendLinkBySms = false;
        this.documentVideo = false;
        this.handleChangeDocumentName =
            this.handleChangeDocumentName.bind(this);
        this.handleChangeValue = this.handleChangeValue.bind(this);
        this.handleChangeSmartReminder =
            this.handleChangeSmartReminder.bind(this);
        this.handleChangeSendLinkBySms =
            this.handleChangeSendLinkBySms.bind(this);
        this.handleAddVideo = this.handleAddVideo.bind(this);
        this.handleRemoveVideo = this.handleRemoveVideo.bind(this);
    }
    render() {
        return [
            h("div", { key: '2689f426c907bf20f2a2cafc580706b659b887b0', class: "send-document-container" }, h("div", { key: '379412a5b1f45019f3da3e2fd91ddd73a013211f', class: "send-document-prepare-container" }, h("h3", { key: 'fbec25ce8cde760e4f8d814abde88c49ba254bc3' }, "Prepare sending"), h("limel-flex-container", { key: '608386d749466bcf679757e49b8a676efd9d91b0', align: "stretch" }, h("limel-input-field", { key: 'e66bd6c90c21efab3c83b4fbfbd59f1c0300f894', label: "Document Name", value: this.documentName, onChange: this.handleChangeDocumentName }), h("limel-input-field", { key: '4e279e1407868ed91bbf2d4f0cd553e4fc61ef94', label: "Value", value: this.value.toString(), onChange: this.handleChangeValue })), h("div", { key: '08444f9990860dea9f772cfb4db8667e2970db58' }, h("h4", { key: 'aa9cb0c7720b2544e6eb9454d46dcdf875974afd' }, "Document engagement"), this.documentVideo ? (h("div", null, h("div", { class: "video-is-added" }, h("limel-icon", { name: "tv_show", size: "large", class: "video-is-added-icon" }), h("span", null, "Video is added"), h("limel-icon", { class: "video-remove-icon", name: "multiply", size: "small", onClick: this.handleRemoveVideo })))) : (h("limel-button", { class: "add-video-button", primary: true, label: "Add Video introduction", onClick: this.handleAddVideo })), h("limel-checkbox", { key: 'f8bf955c735235ec6b3f0e8f54b9c55594fcf73f', label: "Send smart reminders", id: "SmartReminder", checked: this.smartReminder, onChange: this.handleChangeSmartReminder }), h("limel-checkbox", { key: '90e9ad57aba3470610438cab6d499eb2700e7913', label: "Send link by SMS", id: "SendLinkBySMS", checked: this.sendLinkBySms, onChange: this.handleChangeSendLinkBySms }))), h("div", { key: 'd932d8a05b0545ad6627bfe868083db78f6a76c5', class: "send-document-email-container" }, h("create-email", { key: '7aa4c99f1dd64cb1f045bdd47eb84f42e211d63c', document: this.document }))),
        ];
    }
    async loadObjectValue() {
        // eslint-disable-next-line camelcase
        const { id: record_id, limetype } = this.context;
        try {
            const value = await fetchDealValue(this.platform, this.session, limetype, record_id);
            this.setDocumentValue.emit(value);
        }
        catch (e) {
            this.errorHandler.emit('Could not fetch lime object...');
        }
    }
    fileName() {
        if (this.limeDocument) {
            return this.limeDocument.text;
        }
        else if (this.template) {
            return this.template.text;
        }
        else {
            return '';
        }
    }
    handleChangeDocumentName(event) {
        this.setNewDocumentName.emit(event.detail);
    }
    handleChangeValue(event) {
        this.setDocumentValue.emit(event.detail);
    }
    handleChangeSmartReminder(event) {
        this.setSmartReminder.emit(event.detail);
    }
    handleChangeSendLinkBySms(event) {
        this.setIsSmsSending.emit(event.detail);
    }
    handleAddVideo() {
        // should open select video view
        this.changeView.emit(EnumViews.videoLibrary);
    }
    // TODO: function for uploading file, in advance
    // private async handleChange(event: CustomEvent<FileInfo>) {
    //     this.fileValue = event.detail;
    //     const { data, success } = await uploadFile(
    //         this.platform,
    //         this.session,
    //         this.fileValue
    //     );
    //     console.log(data, success);
    // }
    handleRemoveVideo() {
        this.removeVideo.emit();
        this.documentVideo = false;
    }
    static get is() { return "layout-send-document"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-send-document.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-send-document.css"]
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
                    "text": ""
                }
            }
        };
    }
    static get states() {
        return {
            "documentName": {},
            "value": {},
            "smartReminder": {},
            "sendLinkBySms": {},
            "documentVideo": {}
        };
    }
    static get events() {
        return [{
                "method": "setNewDocumentName",
                "name": "setNewDocumentName",
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
                "method": "setDocumentValue",
                "name": "setDocumentValue",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "number",
                    "resolved": "number",
                    "references": {}
                }
            }, {
                "method": "setIsSmsSending",
                "name": "setIsSmsSending",
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
                "method": "setSmartReminder",
                "name": "setSmartReminder",
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
                "method": "removeVideo",
                "name": "removeVideo",
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
//# sourceMappingURL=layout-send-document.js.map
