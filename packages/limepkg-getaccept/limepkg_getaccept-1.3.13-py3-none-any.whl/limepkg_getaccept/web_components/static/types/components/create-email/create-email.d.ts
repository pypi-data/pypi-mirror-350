import { EventEmitter } from '../../stencil-public-runtime';
import { IDocument } from '../../types/Document';
export declare class CreateEmail {
    document: IDocument;
    setEmailSubject: EventEmitter;
    setEmailMessage: EventEmitter;
    private emailSubject;
    private emailMessage;
    componentWillLoad(): void;
    constructor();
    render(): any[];
    private handleChangeEmailSubject;
    private handleChangeEmailMessage;
}
