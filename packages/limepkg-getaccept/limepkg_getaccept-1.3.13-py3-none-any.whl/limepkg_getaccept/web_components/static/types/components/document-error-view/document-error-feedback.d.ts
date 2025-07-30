import { IError } from '../../types/Error';
import { IDocument } from '../../types/Document';
export declare class DocumentErrorFeedback {
    document: IDocument;
    errorList: IError[];
    render(): any[];
}
