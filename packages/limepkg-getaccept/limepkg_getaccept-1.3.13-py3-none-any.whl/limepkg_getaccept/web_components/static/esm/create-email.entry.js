import { r as registerInstance, c as createEvent, h } from './index-0b1d787f.js';

const createEmailCss = ".send-document-email{width:calc(100% - 1.2rem);border-color:rgba(0, 0, 0, 0.12);font-size:0.875rem;line-height:1.125rem;font-weight:400;padding:0.5rem}.send-document-email:focus{outline:none;border-color:#26a69a}.send-document-email-subject{margin-top:1rem;display:block;margin-left:1rem;font-size:0.675rem}";
const CreateEmailStyle0 = createEmailCss;

const CreateEmail = class {
    componentWillLoad() {
        this.emailSubject = this.document.email_send_subject;
        this.emailMessage = this.document.email_send_message;
    }
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.setEmailSubject = createEvent(this, "setEmailSubject", 7);
        this.setEmailMessage = createEvent(this, "setEmailMessage", 7);
        this.document = undefined;
        this.emailSubject = '';
        this.emailMessage = '';
        this.handleChangeEmailSubject =
            this.handleChangeEmailSubject.bind(this);
        this.handleChangeEmailMessage =
            this.handleChangeEmailMessage.bind(this);
    }
    render() {
        return [
            h("div", { key: '1d5599e24eb0c74fc2c258d17dd4bd663d83e3c2' }, h("h3", { key: '691a738cc762ba2b7254895120d3730275c939d7' }, "Write your email"), h("limel-input-field", { key: 'dcefe2d64ff7ad88cff2f446855ab8a961495eca', label: "Subject", value: this.emailSubject, onChange: this.handleChangeEmailSubject }), h("span", { key: 'b9437369529832f80081e9e4fa1dd86497ae33b6', class: "send-document-email-subject" }, "Email"), h("textarea", { key: '8b4f347aaa67bfbe405d7f82037f0268fa31fad3', class: "send-document-email", rows: 9, value: this.emailMessage, onChange: this.handleChangeEmailMessage })),
        ];
    }
    handleChangeEmailSubject(event) {
        this.emailSubject = event.detail;
        this.setEmailSubject.emit(event.detail);
    }
    handleChangeEmailMessage(event) {
        this.setEmailMessage.emit(event.target.value);
    }
};
CreateEmail.style = CreateEmailStyle0;

export { CreateEmail as create_email };

//# sourceMappingURL=create-email.entry.js.map