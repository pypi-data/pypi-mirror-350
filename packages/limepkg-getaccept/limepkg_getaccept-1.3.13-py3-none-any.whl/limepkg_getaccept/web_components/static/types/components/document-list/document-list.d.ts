import { EventEmitter } from '../../stencil-public-runtime';
import { IDocument } from '../../types/Document';
export declare class DocumentList {
    documents: IDocument[];
    intervalId: any;
    loadRelatedDocuments: EventEmitter;
    componentWillLoad(): void;
    disconnectedCallback(): void;
    render(): any;
}
