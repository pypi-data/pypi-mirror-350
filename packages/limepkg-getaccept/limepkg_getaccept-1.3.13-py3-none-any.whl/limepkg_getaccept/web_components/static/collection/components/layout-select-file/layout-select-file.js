/* eslint-disable camelcase */
import { h, } from "@stencil/core";
import { fetchTemplates, fetchLimeDocuments, fetchTemplateFields, fetchObjectProps, fetchTemplateRoles, } from "../../services";
var EnumSections;
(function (EnumSections) {
    EnumSections["None"] = "none";
    EnumSections["Template"] = "template";
    EnumSections["LimeDocuments"] = "limeDocuments";
})(EnumSections || (EnumSections = {}));
export class LayoutSelectFile {
    constructor() {
        this.onChange = (event) => {
            this.currentTab = event.detail.id;
        };
        this.platform = undefined;
        this.context = undefined;
        this.session = undefined;
        this.selectedTemplate = undefined;
        this.selectedLimeDocument = undefined;
        this.customFields = [];
        this.templateRoles = [];
        this.isLoadingTemplates = false;
        this.isLoadingProps = false;
        this.templates = [];
        this.isLoadingFields = false;
        this.isLoadingLimeDocuments = undefined;
        this.limeDocuments = undefined;
        this.openSection = EnumSections.Template;
        this.tableData = [];
        this.currentTab = '1';
        this.gaMergeFields = [
            {
                field: '{{recipient.first_name}}',
                value: 'Recipient - First name',
            },
            {
                field: '{{recipient.last_name}}',
                value: 'Recipient - Last name',
            },
            {
                field: '{{recipient.email}}',
                value: 'Recipient - Email',
            },
            {
                field: '{{recipient.company_name}}',
                value: 'Recipient - Company name',
            },
            {
                field: '{{sender.first_name}}',
                value: 'Sender - First name',
            },
            {
                field: '{{sender.last_name}}',
                value: 'Sender - Last name',
            },
            {
                field: '{{sender.fullname}}',
                value: 'Sender - Full name',
            },
            {
                field: '{{document.name}}',
                value: 'Document - Name',
            },
            {
                field: '{{document.field}}',
                value: 'Document - field',
            },
        ];
        this.loadTemplates = this.loadTemplates.bind(this);
        this.loadTemplateFields = this.loadTemplateFields.bind(this);
        this.loadLimeDocuments = this.loadLimeDocuments.bind(this);
        this.onChangeSection = this.onChangeSection.bind(this);
        this.setTemplates = this.setTemplates.bind(this);
        this.setLimeDocuments = this.setLimeDocuments.bind(this);
        this.setFields = this.setFields.bind(this);
        this.onActivateRow = this.onActivateRow.bind(this);
        this.loadTemplateRoles = this.loadTemplateRoles.bind(this);
    }
    render() {
        return [
            h("div", { key: 'c31131567b868b7b5def65722762e453812ca08a', class: "layout-select-file-container" }, h("h3", { key: '8ed693a1163365bd934b61d80a88017e0b5d3f0f' }, "Select file to send"), h("div", { key: '064743ee88673533791a5f1ca791f8f66498993e', class: "select-file-container" }, h("div", { key: '3b29dafc7dc851d9d1748720fefcad1047fdb512', class: "file-column" }, h("limel-collapsible-section", { key: '31eebc561de57dd1383a8d92c5309ea64545ef3a', header: "Templates", isOpen: this.openSection === EnumSections.Template, onOpen: event => this.onChangeSection(event, EnumSections.Template), onClose: event => this.onChangeSection(event, EnumSections.None) }, h("template-list", { key: '62747af260208b3b3fc2899efb8b223675c764b7', templates: this.templates, selectedTemplate: this.selectedTemplate, isLoading: this.isLoadingTemplates })), h("limel-collapsible-section", { key: '4a714fd3e10d81b8ef4907722e3cba19a53aa9f9', header: "Lime documents", isOpen: this.openSection === EnumSections.LimeDocuments, onOpen: event => this.onChangeSection(event, EnumSections.LimeDocuments), onClose: event => this.onChangeSection(event, EnumSections.None) }, h("lime-document-list", { key: '922c738414c0735f641224f1323288056ea90cf2', documents: this.limeDocuments, selectedLimeDocument: this.selectedLimeDocument, isLoading: this.isLoadingLimeDocuments }))), h("div", { key: 'aba6163aa79ea51dcbe8b81fc097fa2312f1ddc6', class: "file-column" }, h("template-preview", { key: '6278a5d9c833a8e9bb57fd84d1c3508c634f2c68', template: this.selectedTemplate, isLoading: this.isLoadingFields, session: this.session }), h("custom-fields", { key: '0e84430ba774c2d0ce0c11fe7ecce11a58466d8e', template: this.selectedTemplate, customFields: this.customFields, isLoading: this.isLoadingFields }))), !this.isLoadingProps ? (h("limel-collapsible-section", { header: "Show template parameters", onClose: event => event.stopPropagation() }, h("limel-button-group", { onChange: this.onChange, value: [
                    {
                        id: '1',
                        title: 'Template fields',
                        selected: true,
                    },
                    {
                        id: '2',
                        title: 'GetAccept template fields',
                    },
                ] }), this.currentTab === '1' ? (h("table", { class: "merge-fields-table", id: "merge-fields" }, h("thead", null, h("tr", null, h("th", null, "Merge tag"), h("th", null, "Value"), h("th", null))), h("tbody", null, this.tableData.map(value => (h("tr", null, h("td", null, value.field), h("td", null, value.value), h("td", null, h("limel-button", { label: "Copy", primary: true, onClick: () => this.copyToClipboard(value.field) }, "Copy")))))))) : (h("table", { class: "merge-fields-table", id: "getaccept-merge-fields" }, h("thead", null, h("tr", null, h("th", null, "Merge tag"), h("th", null, "Value"), h("th", null))), h("tbody", null, this.gaMergeFields.map(value => (h("tr", null, h("td", null, value.field), h("td", null, value.value), h("td", null, h("limel-button", { label: "Copy", primary: true, onClick: () => this.copyToClipboard(value.field) }, "Copy")))))))))) : (h("limel-spinner", null))),
        ];
    }
    async componentWillLoad() {
        this.loadTemplates().then(() => { });
        this.loadLimeDocuments().then(() => { });
        this.loadObjectProps().then(() => { });
    }
    onChangeSection(event, section) {
        event.stopPropagation();
        this.openSection = section;
    }
    async loadTemplates() {
        this.isLoadingTemplates = true;
        try {
            this.templates = await fetchTemplates(this.platform, this.session, this.selectedTemplate);
        }
        catch (e) {
            this.errorHandler.emit('Could not load templates from GetAccept...');
        }
        this.isLoadingTemplates = false;
    }
    async loadLimeDocuments() {
        this.isLoadingLimeDocuments = true;
        const { id: record_id, limetype } = this.context;
        try {
            this.limeDocuments = await fetchLimeDocuments(this.platform, limetype, record_id, this.selectedLimeDocument);
        }
        catch (e) {
            this.errorHandler.emit('Could not load related Lime documents...');
        }
        this.isLoadingLimeDocuments = false;
    }
    async loadTemplateFields() {
        if (!this.selectedTemplate) {
            this.customFields = [];
            this.setCustomFields.emit(this.customFields);
            return;
        }
        this.isLoadingFields = true;
        const { id: record_id, limetype } = this.context;
        try {
            const fields = await fetchTemplateFields(this.platform, this.session, limetype, record_id, this.selectedTemplate);
            this.setFields(fields);
        }
        catch (e) {
            this.errorHandler.emit('Could not fetch template fields from GetAccept...');
        }
        this.isLoadingFields = false;
    }
    async loadObjectProps() {
        const { id: record_id, limetype } = this.context;
        this.isLoadingProps = true;
        try {
            const props = await fetchObjectProps(this.platform, this.session, limetype, record_id);
            this.setAvailableFields(props);
        }
        catch (e) {
            this.errorHandler.emit('Could not fetch lime object...');
        }
        this.isLoadingProps = false;
    }
    async loadTemplateRoles() {
        if (!this.selectedTemplate) {
            return;
        }
        const { id: record_id, limetype } = this.context;
        try {
            const roles = await fetchTemplateRoles(this.platform, this.session, limetype, record_id, this.selectedTemplate);
            this.setRoles(roles);
        }
        catch (e) {
            this.errorHandler.emit('Could not fetch template roles from GetAccept...');
        }
    }
    setAvailableFields(limeObject) {
        Object.entries(limeObject).forEach(([key, value]) => {
            if (value) {
                this.tableData.push({
                    field: `{{${key}}}`,
                    value: value,
                });
            }
        });
    }
    setFields(fields) {
        const customFields = fields.map(this.mapField);
        this.setCustomFields.emit(customFields);
    }
    setRoles(roles) {
        this.setTemplateRoles.emit(roles);
    }
    onChangeTemplate(data) {
        this.setTemplates(data);
        if (data) {
            this.loadTemplateFields();
            this.loadTemplateRoles();
        }
    }
    setTemplates(template) {
        this.templates = this.getSelectedListItems(this.templates, template);
    }
    onChangeDocument(data) {
        this.setLimeDocuments(data);
    }
    mapField(field) {
        return {
            value: field.field_value.toString(),
            id: field.field_id,
            label: field.field_label,
            is_editable: field.is_editable === null ? true : field.is_editable,
        };
    }
    setLimeDocuments(document) {
        this.limeDocuments = this.getSelectedListItems(this.limeDocuments, document);
    }
    getSelectedListItems(items, selectedItem) {
        return items.map((item) => {
            if (selectedItem && item.value === selectedItem.value) {
                return selectedItem;
            }
            return Object.assign(Object.assign({}, item), { selected: false });
        });
    }
    updateFieldValue(event) {
        const { id, value } = event.detail;
        const customFields = this.customFields.map(field => {
            return field.id === id ? Object.assign(Object.assign({}, field), { value: value }) : field;
        });
        this.setCustomFields.emit(customFields);
    }
    onActivateRow(event) {
        navigator.clipboard.writeText(event.detail.field);
        this.errorHandler.emit(`Copied '${event.detail.field}' to your clipboard`);
    }
    copyToClipboard(text) {
        navigator.clipboard.writeText(text);
        this.errorHandler.emit(`Copied '${text}' to your clipboard`);
    }
    static get is() { return "layout-select-file"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-select-file.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-select-file.css"]
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
            "selectedTemplate": {
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
            "selectedLimeDocument": {
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
            "customFields": {
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
                },
                "defaultValue": "[]"
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
                },
                "defaultValue": "[]"
            }
        };
    }
    static get states() {
        return {
            "isLoadingTemplates": {},
            "isLoadingProps": {},
            "templates": {},
            "isLoadingFields": {},
            "isLoadingLimeDocuments": {},
            "limeDocuments": {},
            "openSection": {},
            "tableData": {},
            "currentTab": {},
            "gaMergeFields": {}
        };
    }
    static get events() {
        return [{
                "method": "setCustomFields",
                "name": "setCustomFields",
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
                "method": "setTemplateRoles",
                "name": "setTemplateRoles",
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
    static get watchers() {
        return [{
                "propName": "selectedTemplate",
                "methodName": "onChangeTemplate"
            }, {
                "propName": "selectedLimeDocument",
                "methodName": "onChangeDocument"
            }];
    }
    static get listeners() {
        return [{
                "name": "updateFieldValue",
                "method": "updateFieldValue",
                "target": undefined,
                "capture": false,
                "passive": false
            }];
    }
}
//# sourceMappingURL=layout-select-file.js.map
