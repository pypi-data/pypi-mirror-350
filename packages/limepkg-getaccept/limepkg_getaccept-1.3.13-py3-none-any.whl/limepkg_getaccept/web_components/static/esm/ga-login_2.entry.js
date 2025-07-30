import { r as registerInstance, c as createEvent, h } from './index-0b1d787f.js';
import { P as PlatformServiceName, o as signup } from './index-fd1933d7.js';

const gaLoginCss = ".auth-error{display:block;color:#f88987;margin-top:1rem}.auth-button{margin-top:1rem}limel-button{--lime-primary-color:#f49132}";
const GaLoginStyle0 = gaLoginCss;

const GaLogin = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.setSession = createEvent(this, "setSession", 7);
        this.loginFields = [
            {
                id: 'LoginEmail',
                style: 'auth-imput',
                label: 'Email address',
                type: 'email',
                value: 'email',
                required: false,
                icon: 'filled_message',
            },
            {
                id: 'LoginPassword',
                style: 'auth-imput',
                label: 'Password',
                type: 'password',
                value: 'password',
                required: false,
                icon: 'lock_2',
            },
        ];
        this.platform = undefined;
        this.loading = false;
        this.errorOnLogin = false;
        this.email = '';
        this.password = '';
        this.onChange = this.onChange.bind(this);
        this.onLogin = this.onLogin.bind(this);
        this.isDisabled = this.isDisabled.bind(this);
    }
    render() {
        return [
            this.loginFields.map((loginField) => {
                return (h("limel-input-field", { id: loginField.id, class: loginField.style, label: loginField.label, type: loginField.type, value: this[loginField.value], required: loginField.required, trailingIcon: loginField.icon, onChange: (event) => this.onChange(event, loginField.value) }));
            }),
            (() => {
                return (h("div", null, h("limel-button", { class: "auth-button", label: "Login", primary: true, loading: this.loading, disabled: this.isDisabled(), onClick: this.onLogin }), this.errorOnLogin ? (h("span", { class: "auth-error" }, "Could not login. Please check your credentials")) : null));
            })(),
        ];
    }
    isDisabled() {
        return !(this.email && this.password);
    }
    onChange(event, valueReference) {
        this[valueReference] = event.detail;
    }
    async onLogin() {
        this.errorOnLogin = false;
        this.loading = true;
        const data = { email: this.email, password: this.password };
        const response = await this.platform
            .get(PlatformServiceName.Http)
            .post('getaccept/login/', data);
        this.loading = false;
        if (response.success) {
            const session = {
                username: this.email,
                access_token: response.data.access_token,
                expires_in: response.data.expires_in,
            };
            this.setSession.emit(session);
        }
        else {
            this.errorOnLogin = true;
        }
    }
};
GaLogin.style = GaLoginStyle0;

const gaSignupCss = ".auth-signup-field-container{display:flex;flex-wrap:wrap}.auth-imput{margin-bottom:0.2rem;margin-right:0.5rem;width:48%}.auth-button{margin-top:1rem}.auth-imput{margin-bottom:0.2rem}.auth-language-label{display:block;margin:1rem 0rem 0.5rem 1rem}limel-button{--lime-primary-color:#f49132}";
const GaSignupStyle0 = gaSignupCss;

const GaSignup = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.setSession = createEvent(this, "setSession", 7);
        this.errorHandler = createEvent(this, "errorHandler", 7);
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
};
GaSignup.style = GaSignupStyle0;

export { GaLogin as ga_login, GaSignup as ga_signup };

//# sourceMappingURL=ga-login_2.entry.js.map