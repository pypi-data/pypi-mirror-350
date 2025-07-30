'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const gaLoaderCss = "limel-spinner{margin:1rem 0;color:#f49132}";
const GaLoaderStyle0 = gaLoaderCss;

const GALoader = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
    }
    render() {
        return (index.h("limel-flex-container", { key: 'aa79d9910c1fe5481c66bea8cc8bf00f104fda23', justify: "center" }, index.h("limel-spinner", { key: '88bc1183e4fcca0f8b6811bf3819d86078cd1aef' })));
    }
};
GALoader.style = GaLoaderStyle0;

exports.ga_loader = GALoader;

//# sourceMappingURL=ga-loader.cjs.entry.js.map