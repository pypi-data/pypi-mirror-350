import { h } from "@stencil/core";
export class GALoader {
    render() {
        return (h("limel-flex-container", { key: 'aa79d9910c1fe5481c66bea8cc8bf00f104fda23', justify: "center" }, h("limel-spinner", { key: '88bc1183e4fcca0f8b6811bf3819d86078cd1aef' })));
    }
    static get is() { return "ga-loader"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["ga-loader.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["ga-loader.css"]
        };
    }
}
//# sourceMappingURL=ga-loader.js.map
