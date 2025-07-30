'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const menuButtonCss = ".ga-menu-item{display:flex;flex-direction:row;cursor:pointer;padding:0.5rem}.ga-menu-item:hover{background-color:#f49132;color:#fff}.ga-menu-item .menu-icon{margin-right:0.2rem;font-size:0.6rem}";
const MenuButtonStyle0 = menuButtonCss;

const MenuButton = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.closeMenu = index.createEvent(this, "closeMenu", 7);
        this.menuItem = undefined;
        this.handleMenuClick = this.handleMenuClick.bind(this);
    }
    render() {
        const { icon, label, view } = this.menuItem;
        return (index.h("li", { key: '947319378e0021a2e06223c6eb325011b200d99f', class: "ga-menu-item", onClick: () => this.handleMenuClick(view) }, index.h("limel-icon", { key: '95b2adf0cc36259544a6baccfbf5006f5a95fdcc', class: "menu-icon", name: icon, size: "small" }), index.h("span", { key: '986bc65df73709dd726a19512f5fd8c64f6e70ad' }, label)));
    }
    handleMenuClick(view) {
        this.changeView.emit(view);
        this.closeMenu.emit(false);
    }
};
MenuButton.style = MenuButtonStyle0;

exports.menu_button = MenuButton;

//# sourceMappingURL=menu-button.cjs.entry.js.map