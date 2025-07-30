import { r as registerInstance, c as createEvent, h } from './index-0b1d787f.js';

const menuButtonCss = ".ga-menu-item{display:flex;flex-direction:row;cursor:pointer;padding:0.5rem}.ga-menu-item:hover{background-color:#f49132;color:#fff}.ga-menu-item .menu-icon{margin-right:0.2rem;font-size:0.6rem}";
const MenuButtonStyle0 = menuButtonCss;

const MenuButton = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.closeMenu = createEvent(this, "closeMenu", 7);
        this.menuItem = undefined;
        this.handleMenuClick = this.handleMenuClick.bind(this);
    }
    render() {
        const { icon, label, view } = this.menuItem;
        return (h("li", { key: '947319378e0021a2e06223c6eb325011b200d99f', class: "ga-menu-item", onClick: () => this.handleMenuClick(view) }, h("limel-icon", { key: '95b2adf0cc36259544a6baccfbf5006f5a95fdcc', class: "menu-icon", name: icon, size: "small" }), h("span", { key: '986bc65df73709dd726a19512f5fd8c64f6e70ad' }, label)));
    }
    handleMenuClick(view) {
        this.changeView.emit(view);
        this.closeMenu.emit(false);
    }
};
MenuButton.style = MenuButtonStyle0;

export { MenuButton as menu_button };

//# sourceMappingURL=menu-button.entry.js.map