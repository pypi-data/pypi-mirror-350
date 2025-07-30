import { EventEmitter } from '../../stencil-public-runtime';
export declare class Root {
    isSigning: boolean;
    changeView: EventEmitter;
    setDocumentType: EventEmitter<boolean>;
    private buttonData;
    constructor();
    render(): any[];
    private changeViewHandler;
}
