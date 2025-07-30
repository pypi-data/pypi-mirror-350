import { h } from "@stencil/core";
export class LayoutLogin {
    constructor() {
        this.platform = undefined;
        this.isSignup = false;
        this.toggleSignupContainer = this.toggleSignupContainer.bind(this);
    }
    render() {
        const loginClass = this.isSignup
            ? 'login-container'
            : 'login-container active';
        const signupClass = this.isSignup
            ? 'signup-container active'
            : 'signup-container';
        return [
            h("div", { key: 'fc6aec64a7de5ca7bde59e619da22ffe81582c77', class: "auth-container" }, h("div", { key: '94e74eff2ddcbf1fb3ba523943a0174b578cbd20', class: loginClass, onClick: () => this.toggleSignupContainer(false) }, h("h3", { key: '5b1810ed01cd4891156c5b591de572f7d5b7055b' }, "Welcome Back"), h("ga-login", { key: '21bc30f0b611229f0cddd21b29dee8c2b103c290', platform: this.platform })), h("div", { key: 'c2b31cb9c3f9f91a9f9bf1f94c36bae4407f055d', class: signupClass, onClick: () => this.toggleSignupContainer(true) }, h("h3", { key: '3d88d65d13857e1a009f2253af1869cfcc590c94' }, "Create Account"), (() => {
                if (this.isSignup) {
                    return h("ga-signup", { platform: this.platform });
                }
                else {
                    return (h("limel-input-field", { label: "Email address", type: "email", value: "", trailingIcon: "filled_message" }));
                }
            })())),
        ];
    }
    toggleSignupContainer(value) {
        this.isSignup = value;
    }
    static get is() { return "layout-login"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-login.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-login.css"]
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
            "isSignup": {}
        };
    }
}
//# sourceMappingURL=layout-login.js.map
