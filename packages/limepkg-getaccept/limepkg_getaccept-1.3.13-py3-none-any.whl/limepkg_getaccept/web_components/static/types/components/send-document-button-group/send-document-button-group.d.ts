import { EventEmitter } from '../../stencil-public-runtime';
export declare class SendDocumentButtonGroup {
    validateDocument: EventEmitter<boolean>;
    private disabled;
    private loading;
    constructor();
    render(): any[];
    private handleOnClickSendButton;
}
