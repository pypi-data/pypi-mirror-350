/* eslint-disable camelcase */
import { h, } from "@stencil/core";
import { PlatformServiceName, } from "@limetech/lime-web-components";
export class LayoutSelectRecipient {
    async componentWillLoad() {
        this.selectedRecipientList = this.document.recipients;
        if (this.selectedRecipientList.length < 1) {
            const currentPersons = await this.fetchCurrentPersons();
            currentPersons.forEach(recipient => {
                this.selectRecipientHandler(recipient);
            });
        }
    }
    constructor() {
        this.platform = undefined;
        this.document = undefined;
        this.context = undefined;
        this.isAside = false;
        this.searchTerm = undefined;
        this.selectedRecipientList = [];
        this.includeCoworkers = false;
        this.recipientList = [];
        this.selectRecipientHandler = this.selectRecipientHandler.bind(this);
        this.isAdded = this.isAdded.bind(this);
        this.onSearch = this.onSearch.bind(this);
        this.toggleIncludeCoworkers = this.toggleIncludeCoworkers.bind(this);
        this.fetchRecipients = this.fetchRecipients.bind(this);
        this.fetchCurrentPersons = this.fetchCurrentPersons.bind(this);
    }
    render() {
        return [
            h("div", { key: '5daef11e3a183814a926363b0f5163fa6327ec2c', class: {
                    'select-recipient-container': true,
                    aside: this.isAside,
                } }, h("div", { key: '9c4325c9056cc0f062b58494903448208fe19bee', class: "recipient-container" }, h("h3", { key: '0fbabccf0ba5271e3855171e1f3e054ae3a494ab' }, "Search Recipient"), h("div", { key: '0aa8afffc25e1f81ea28bf4a8986e5a58b35929f', class: "recipient-toolbar" }, h("limel-input-field", { key: 'ea70c6313bd1fb993ec3634dfb3fff6313d55929', label: "Search recipient", value: this.searchTerm, onChange: this.onSearch }), h("limel-switch", { key: 'f915b7cd8a456516ab2c260de5a8c249440e8520', label: "Include coworkers", value: this.includeCoworkers, onChange: this.toggleIncludeCoworkers })), h("ul", { key: '5011cbd2bdaef05d58ddb7026f2b458ae95b9bab', class: "recipient-list" }, this.recipientList.map(recipient => {
                if (!this.isAdded(recipient.lime_id)) {
                    return (h("recipient-item", { recipient: recipient, showAdd: true, onClick: () => {
                            this.selectRecipientHandler(recipient);
                        } }));
                }
            }))), h("div", { key: '0e0e3f078a48f6f28f843339e7864f9f7294bb96', class: "selected-recipient-container" }, h("h3", { key: '0fc33d45d42bea13da5fe8e856772bb3698ab8d1' }, "Added recipients"), h("selected-recipient-list", { key: '3c6cb39e6034f1294a3c49a333374fa49d2f278e', recipients: this.selectedRecipientList, document: this.document }))),
        ];
    }
    selectRecipientHandler(recipient) {
        if (!!recipient.mobile || !!recipient.email) {
            this.selectedRecipientList = [
                ...this.selectedRecipientList,
                recipient,
            ];
            this.updateDocumentRecipient.emit(this.selectedRecipientList);
        }
        else {
            this.errorHandler.emit('A recipient needs to have a mobile number or an email address');
        }
    }
    removeRecipientHandler(recipient) {
        const rec = recipient.detail;
        this.selectedRecipientList = this.selectedRecipientList.filter(recipientData => {
            return recipientData.lime_id !== rec.lime_id;
        });
        this.updateDocumentRecipient.emit(this.selectedRecipientList);
        this.onSearch({ detail: '' });
    }
    changeRecipientRoleHandler(recipient) {
        const recipientData = recipient.detail;
        const index = this.selectedRecipientList.findIndex(rec => rec.lime_id === recipientData.lime_id);
        this.selectedRecipientList[index] = recipientData;
        this.updateDocumentRecipient.emit(this.selectedRecipientList);
    }
    isAdded(recipientId) {
        return !!this.selectedRecipientList.find(recipient => recipient.lime_id === recipientId);
    }
    toggleIncludeCoworkers() {
        this.includeCoworkers = !this.includeCoworkers;
        this.fetchRecipients();
    }
    async onSearch(event) {
        this.searchTerm = event.detail;
        this.fetchRecipients();
    }
    async fetchRecipients() {
        const options = {
            params: {
                search: this.searchTerm,
                limit: '10',
                offset: '0',
            },
        };
        try {
            const persons = await this.fetchPersons(options);
            const coworkers = await this.fetchCoworkers(options, this.includeCoworkers);
            this.recipientList = [...persons, ...coworkers];
        }
        catch (e) {
            this.errorHandler.emit('Something went wrong while communicating with the server...');
        }
    }
    async fetchPersons(options) {
        const persons = await this.platform
            .get(PlatformServiceName.Http)
            .get('getaccept/persons', options);
        return persons.map(person => (Object.assign(Object.assign({}, person), { fullname: `${person.first_name} ${person.last_name}` })));
    }
    async fetchCurrentPersons() {
        const { id: record_id, limetype } = this.context;
        const options = {
            params: {
                limetype: limetype,
                record_id: record_id.toString(),
            },
        };
        const currentPersons = await this.platform
            .get(PlatformServiceName.Http)
            .get('getaccept/current-persons', options);
        // eslint-disable-next-line sonarjs/no-identical-functions
        return currentPersons.map(person => (Object.assign(Object.assign({}, person), { fullname: `${person.first_name} ${person.last_name}` })));
    }
    async fetchCoworkers(options, includeCoworkers) {
        if (!includeCoworkers) {
            return [];
        }
        const coworkers = await this.platform
            .get(PlatformServiceName.Http)
            .get('getaccept/coworkers', options);
        return coworkers.map(coworker => (Object.assign(Object.assign({}, coworker), { fullname: `${coworker.first_name} ${coworker.last_name}` })));
    }
    static get is() { return "layout-select-recipient"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-select-recipient.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-select-recipient.css"]
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
                    "text": ""
                }
            },
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
            },
            "isAside": {
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
                "attribute": "is-aside",
                "reflect": false,
                "defaultValue": "false"
            }
        };
    }
    static get states() {
        return {
            "searchTerm": {},
            "selectedRecipientList": {},
            "includeCoworkers": {},
            "recipientList": {}
        };
    }
    static get events() {
        return [{
                "method": "updateDocumentRecipient",
                "name": "updateDocumentRecipient",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "IRecipient[]",
                    "resolved": "IRecipient[]",
                    "references": {
                        "IRecipient": {
                            "location": "import",
                            "path": "../../types/Recipient",
                            "id": "src/types/Recipient.ts::IRecipient"
                        }
                    }
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
            }];
    }
    static get listeners() {
        return [{
                "name": "removeRecipient",
                "method": "removeRecipientHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }, {
                "name": "changeRecipientRole",
                "method": "changeRecipientRoleHandler",
                "target": undefined,
                "capture": false,
                "passive": false
            }];
    }
}
//# sourceMappingURL=layout-select-recipient.js.map
