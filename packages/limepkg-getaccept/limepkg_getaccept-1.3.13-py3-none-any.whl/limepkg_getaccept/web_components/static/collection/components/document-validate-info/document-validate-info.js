import { h } from "@stencil/core";
export class DocumentValidateInfo {
    constructor() {
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
    static get is() { return "document-validate-info"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["document-validate-info.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["document-validate-info.css"]
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
            }
        };
    }
}
//# sourceMappingURL=document-validate-info.js.map
