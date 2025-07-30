'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const customFieldsCss = ".custom-field{margin-top:1rem}";
const CustomFieldsStyle0 = customFieldsCss;

const CustomFields = class {
    constructor(hostRef) { index.registerInstance(this, hostRef); this.updateFieldValue = index.createEvent(this, "updateFieldValue", 7); this.template = undefined; this.customFields = undefined; this.isLoading = undefined; }
    render() {
        if (this.isLoading) {
            return index.h("ga-loader", null);
        }
        else if (!this.template) {
            return [];
        }
        if (!this.customFields.length) {
            return [
                index.h("h4", null, "Fields"),
                index.h("empty-state", { text: "This template has no fields", icon: "text_box" }),
            ];
        }
        return [
            index.h("h4", null, "Fields"),
            this.customFields.map(field => (index.h("limel-input-field", { class: "custom-field", label: field.label, value: field.value, disabled: !field.is_editable, onChange: event => this.onChangeField(event, field.id) }))),
        ];
    }
    onChangeField(event, id) {
        this.updateFieldValue.emit({ id: id, value: event.detail });
    }
};
CustomFields.style = CustomFieldsStyle0;

const limeDocumentListCss = ".accordion-content{max-height:25rem;overflow-y:scroll}limel-list{--lime-primary-color:#f49132}";
const LimeDocumentListStyle0 = limeDocumentListCss;

const LimeDocumentList = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setLimeDocument = index.createEvent(this, "setLimeDocument", 7);
        this.documents = [];
        this.selectedLimeDocument = undefined;
        this.isLoading = undefined;
        this.selectDocument = this.selectDocument.bind(this);
    }
    render() {
        console.log(this.documents);
        if (this.isLoading) {
            return index.h("ga-loader", null);
        }
        else if (!this.documents.length) {
            return index.h("empty-state", { text: "No documents were found!" });
        }
        return (index.h("limel-list", { class: "accordion-content", items: this.documents, type: "selectable", onChange: this.selectDocument }));
    }
    selectDocument(event) {
        this.setLimeDocument.emit(event.detail);
    }
};
LimeDocumentList.style = LimeDocumentListStyle0;

const templateListCss = ".accordion-content{max-height:25rem;overflow-y:scroll}limel-list{--lime-primary-color:#f49132}";
const TemplateListStyle0 = templateListCss;

const TemplateList = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setTemplate = index.createEvent(this, "setTemplate", 7);
        this.templates = undefined;
        this.selectedTemplate = undefined;
        this.isLoading = undefined;
        this.selectTemplate = this.selectTemplate.bind(this);
    }
    render() {
        if (this.isLoading) {
            return index.h("ga-loader", null);
        }
        if (!this.templates.length) {
            return index.h("empty-state", { text: "No templates were found!" });
        }
        return (index.h("limel-list", { class: "accordion-content", items: this.templates, type: "selectable", onChange: this.selectTemplate }));
    }
    selectTemplate(event) {
        this.setTemplate.emit(event.detail);
    }
};
TemplateList.style = TemplateListStyle0;

const templatePreviewCss = ".page-info-container{display:flex;justify-content:center}.page-info-container .page-thumb{width:9rem;height:12rem;background-color:#ccc;object-fit:contain}";
const TemplatePreviewStyle0 = templatePreviewCss;

const TemplatePreview = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.template = undefined;
        this.isLoading = undefined;
        this.session = undefined;
        this.getThumbUrl = this.getThumbUrl.bind(this);
    }
    getThumbUrl() {
        const path = `${this.session.entity_id}/${this.template.value}`;
        return `getaccept/preview_proxy/${path}`;
    }
    render() {
        if (!this.template || this.isLoading) {
            return [];
        }
        return (index.h("div", { class: "page-info-container" }, index.h("img", { class: "page-thumb", src: this.template.thumbUrl })));
    }
};
TemplatePreview.style = TemplatePreviewStyle0;

exports.custom_fields = CustomFields;
exports.lime_document_list = LimeDocumentList;
exports.template_list = TemplateList;
exports.template_preview = TemplatePreview;

//# sourceMappingURL=custom-fields_4.cjs.entry.js.map