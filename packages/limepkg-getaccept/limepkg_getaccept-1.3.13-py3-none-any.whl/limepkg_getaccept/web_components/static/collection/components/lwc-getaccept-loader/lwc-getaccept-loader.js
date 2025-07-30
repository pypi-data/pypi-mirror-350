// NOTE: Do NOT remove this component, it is required to run the plugin correctly.
// However, if your plugin has any code that should run only once when the application
// starts, you are free to use the component lifecycle methods below to do so.
// The component should never render anything, so do NOT implement a render method.
export class Loader {
    constructor() {
        this.platform = undefined;
        this.context = undefined;
    }
    connectedCallback() {
        // tslint:disable-line:no-empty
    }
    componentWillLoad() {
        // tslint:disable-line:no-empty
    }
    disconnectedCallback() {
        // tslint:disable-line:no-empty
    }
    componentWillUpdate() {
        // tslint:disable-line:no-empty
    }
    static get is() { return "lwc-getaccept-loader"; }
    static get encapsulation() { return "shadow"; }
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
                    "text": "Reference to the platform"
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
                    "text": "The context this component belongs to"
                }
            }
        };
    }
}
//# sourceMappingURL=lwc-getaccept-loader.js.map
