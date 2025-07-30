import { EventEmitter } from '../../stencil-public-runtime';
import { EnumViews } from '../../models/EnumViews';
export declare class WorkflowProgressBar {
    activeView: EnumViews;
    isVisible: boolean;
    changeView: EventEmitter<EnumViews>;
    constructor();
    render(): any;
    private changeViewHandlerPrevious;
    private changeViewHandlerNext;
    private changeViewSelectedStep;
}
