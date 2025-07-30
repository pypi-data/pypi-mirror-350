/// <reference types="node" />
import { EnumViews } from '../../models/EnumViews';
import { EventEmitter } from 'events';
export declare class LayoutMenu {
    activeView: EnumViews;
    isSending: boolean;
    private menuItems;
    private isOpen;
    changeView: EventEmitter;
    constructor();
    render(): any;
    private toggleMenu;
    private handleBack;
    private onNavigate;
    private onCancelMenu;
    private previousViewOnClose;
    private showBackButton;
}
