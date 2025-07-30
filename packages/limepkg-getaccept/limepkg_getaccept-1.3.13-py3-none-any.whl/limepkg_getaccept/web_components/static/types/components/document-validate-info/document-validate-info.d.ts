import { IDocument } from '../../types/Document';
export declare class DocumentValidateInfo {
    document: IDocument;
    constructor();
    render(): any[];
    hasProperty(value: any): string;
}
