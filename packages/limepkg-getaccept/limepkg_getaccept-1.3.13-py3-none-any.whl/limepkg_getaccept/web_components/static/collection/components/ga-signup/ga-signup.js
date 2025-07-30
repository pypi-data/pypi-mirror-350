import { h } from "@stencil/core";
import { signup } from "../../services";
export class GaSignup {
    constructor() {
        this.signupFields = [
            {
                id: 'SignupEmail',
                style: 'auth-imput',
                label: 'Email address',
                type: 'email',
                value: 'signupEmail',
                required: true,
                icon: 'filled_message',
            },
            {
                id: 'Password',
                style: 'auth-imput',
                label: 'Password',
                type: 'password',
                value: 'signupPassword',
                required: true,
                icon: 'lock_2',
            },
            {
                id: 'FirstName',
                style: 'auth-imput',
                label: 'First name',
                type: 'text',
                value: 'signupFirstName',
                required: true,
                icon: 'user',
            },
            {
                id: 'LastName',
                style: 'auth-imput',
                label: 'Last name',
                type: 'text',
                value: 'signupLastName',
                required: true,
                icon: 'user',
            },
            {
                id: 'Company',
                style: 'auth-imput',
                label: 'Company',
                type: 'text',
                value: 'companyName',
                required: true,
                icon: 'organization',
            },
            {
                id: 'Mobile',
                style: 'auth-imput',
                label: 'Mobile',
                type: 'text',
                value: 'mobile',
                required: true,
                icon: 'phone_not_being_used',
            },
        ];
        this.countryCodes = [
            {
                id: 'SE',
                text: 'SWE',
                selected: true,
            },
            {
                id: 'NO',
                text: 'NOR',
            },
            {
                id: 'FI',
                text: 'FIN',
            },
            {
                id: 'DK',
                text: 'DEN',
            },
            {
                id: 'GB',
                text: 'GBR',
            },
            {
                id: 'US',
                text: 'USA',
            },
        ];
        this.platform = undefined;
        this.isLoading = false;
        this.disableSignup = false;
        this.signupFirstName = '';
        this.signupLastName = '';
        this.companyName = '';
        this.mobile = '';
        this.countryCode = 'SE';
        this.signupEmail = undefined;
        this.signupPassword = '';
        this.onChange = this.onChange.bind(this);
        this.countrySetOnChange = this.countrySetOnChange.bind(this);
        this.onSignup = this.onSignup.bind(this);
    }
    render() {
        this.disableSignup = this.shouldDisableSignup();
        return [
            h("div", { key: 'f078c65ec396cd0c92e4533684e5f180856d9807', class: "auth-signup-field-container" }, this.signupFields.map((signupField) => {
                return (h("limel-input-field", { id: signupField.id, class: signupField.style, label: signupField.label, type: signupField.type, value: this[signupField.value], required: signupField.required, trailingIcon: signupField.icon, onChange: event => this.onChange(event, signupField.value) }));
            })),
            h("span", { key: '81d917ddad7c214074978e7bb3da1793765eb604', class: "auth-language-label" }, "Country"),
            h("limel-chip-set", { key: '9a97a52f9ca83d2cef6a3ef89f184137b0d1c426', type: "choice", onChange: this.countrySetOnChange, required: true, value: this.countryCodes }),
            h("limel-button", { key: 'f202a3d88334c33fd6a7fc570b0b666a7301f017', class: "auth-button", label: "Signup", primary: true, loading: this.isLoading, disabled: this.disableSignup, onClick: this.onSignup }),
        ];
    }
    shouldDisableSignup() {
        return (this.signupEmail === '' &&
            this.signupLastName === '' &&
            this.signupLastName === '' &&
            this.mobile === '' &&
            this.signupPassword === '');
    }
    onChange(event, valueReference) {
        this[valueReference] = event.detail;
    }
    countrySetOnChange(event) {
        this.countryCode = event.detail.id.toString();
    }
    async onSignup() {
        this.isLoading = true;
        const signupData = {
            company: this.companyName,
            first_name: this.signupFirstName,
            last_name: this.signupLastName,
            country_code: this.countryCode,
            mobile: this.mobile,
            email: this.signupEmail,
            password: this.signupPassword,
        };
        const { data, success } = await signup(this.platform, signupData);
        if (success) {
            const session = {
                username: this.signupEmail,
                access_token: data.access_token,
                expires_in: data.expires_in,
            };
            this.setSession.emit(session);
        }
        else {
            if (data.error) {
                this.errorHandler.emit(data.error);
            }
            else {
                this.errorHandler.emit('Something went wrong...');
            }
        }
        this.isLoading = false;
    }
    static get is() { return "ga-signup"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["ga-signup.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["ga-signup.css"]
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
            }
        };
    }
    static get states() {
        return {
            "isLoading": {},
            "disableSignup": {},
            "signupFirstName": {},
            "signupLastName": {},
            "companyName": {},
            "mobile": {},
            "countryCode": {},
            "signupEmail": {},
            "signupPassword": {}
        };
    }
    static get events() {
        return [{
                "method": "setSession",
                "name": "setSession",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
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
}
//# sourceMappingURL=ga-signup.js.map
