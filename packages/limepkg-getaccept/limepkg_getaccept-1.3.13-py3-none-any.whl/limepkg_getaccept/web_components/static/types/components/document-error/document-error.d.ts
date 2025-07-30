import { EventEmitter } from '../../stencil-public-runtime';
import { IError } from '../../types/Error';
import { EnumViews } from '../../models/EnumViews';
export declare class DocumentError {
    error: IError;
    changeView: EventEmitter<EnumViews>;
    constructor();
    render(): any[];
    private onClick;
}
