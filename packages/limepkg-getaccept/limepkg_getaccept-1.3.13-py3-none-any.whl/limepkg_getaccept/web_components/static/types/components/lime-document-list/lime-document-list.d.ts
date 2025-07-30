import { EventEmitter } from '../../stencil-public-runtime';
import { IListItem } from "../../types/ListItem";
export declare class LimeDocumentList {
    documents: any[];
    selectedLimeDocument: IListItem;
    isLoading: boolean;
    setLimeDocument: EventEmitter;
    constructor();
    render(): any;
    private selectDocument;
}
