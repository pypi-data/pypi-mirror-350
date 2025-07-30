import { EventEmitter } from '../../stencil-public-runtime';
import { IDocument } from '../../types/Document';
export declare class DocumentListItem {
    document: IDocument;
    openDocument: EventEmitter<IDocument>;
    constructor();
    render(): any;
    private handleOpenDocument;
    private getDocumentIcon;
}
