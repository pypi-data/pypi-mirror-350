import { EventEmitter } from '../../stencil-public-runtime';
import { IMenuItem } from '../../types/MenuItem';
export declare class MenuButton {
    changeView: EventEmitter;
    closeMenu: EventEmitter;
    menuItem: IMenuItem;
    constructor();
    render(): any;
    private handleMenuClick;
}
