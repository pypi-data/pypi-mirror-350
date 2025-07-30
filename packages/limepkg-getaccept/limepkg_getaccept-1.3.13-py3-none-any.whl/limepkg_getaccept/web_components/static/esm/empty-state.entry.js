import { r as registerInstance, h } from './index-0b1d787f.js';

const emptyStateCss = ".empty-state{margin-top:1.5rem;font-style:italic;text-align:center;opacity:0.8}.empty-state limel-icon{width:3rem;height:3rem}";
const EmptyStateStyle0 = emptyStateCss;

const EmptyState = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.text = undefined;
        this.icon = 'nothing_found';
    }
    render() {
        return (h("div", { key: 'a230f0b89003280afd8206eebb77c5b5b8cd22f2', class: "empty-state" }, h("limel-icon", { key: 'fd224beccacb08c0294787687fe7b40327feb5b9', name: this.icon }), h("p", { key: '84e9d511f1eb14a1bd5b3ac6f75d1c76cc15f63b' }, this.text)));
    }
};
EmptyState.style = EmptyStateStyle0;

export { EmptyState as empty_state };

//# sourceMappingURL=empty-state.entry.js.map