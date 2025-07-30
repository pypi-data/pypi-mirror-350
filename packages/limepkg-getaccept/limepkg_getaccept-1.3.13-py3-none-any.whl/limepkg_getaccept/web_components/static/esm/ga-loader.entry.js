import { r as registerInstance, h } from './index-0b1d787f.js';

const gaLoaderCss = "limel-spinner{margin:1rem 0;color:#f49132}";
const GaLoaderStyle0 = gaLoaderCss;

const GALoader = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
    }
    render() {
        return (h("limel-flex-container", { key: 'aa79d9910c1fe5481c66bea8cc8bf00f104fda23', justify: "center" }, h("limel-spinner", { key: '88bc1183e4fcca0f8b6811bf3819d86078cd1aef' })));
    }
};
GALoader.style = GaLoaderStyle0;

export { GALoader as ga_loader };

//# sourceMappingURL=ga-loader.entry.js.map