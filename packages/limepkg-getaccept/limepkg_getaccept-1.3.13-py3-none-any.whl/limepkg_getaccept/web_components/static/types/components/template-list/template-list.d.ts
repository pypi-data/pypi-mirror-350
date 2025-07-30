import { EventEmitter } from '../../stencil-public-runtime';
import { IListItem } from '../../types/ListItem';
import { ListItem, ListSeparator } from '@limetech/lime-elements';
export declare class TemplateList {
    templates: Array<ListItem | ListSeparator>;
    selectedTemplate: IListItem;
    isLoading: boolean;
    setTemplate: EventEmitter;
    constructor();
    render(): any;
    private selectTemplate;
}
