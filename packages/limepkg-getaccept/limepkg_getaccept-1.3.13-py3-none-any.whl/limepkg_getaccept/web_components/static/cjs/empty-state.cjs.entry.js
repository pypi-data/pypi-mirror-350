'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const emptyStateCss = ".empty-state{margin-top:1.5rem;font-style:italic;text-align:center;opacity:0.8}.empty-state limel-icon{width:3rem;height:3rem}";
const EmptyStateStyle0 = emptyStateCss;

const EmptyState = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.text = undefined;
        this.icon = 'nothing_found';
    }
    render() {
        return (index.h("div", { key: 'a230f0b89003280afd8206eebb77c5b5b8cd22f2', class: "empty-state" }, index.h("limel-icon", { key: 'fd224beccacb08c0294787687fe7b40327feb5b9', name: this.icon }), index.h("p", { key: '84e9d511f1eb14a1bd5b3ac6f75d1c76cc15f63b' }, this.text)));
    }
};
EmptyState.style = EmptyStateStyle0;

exports.empty_state = EmptyState;

//# sourceMappingURL=empty-state.cjs.entry.js.map