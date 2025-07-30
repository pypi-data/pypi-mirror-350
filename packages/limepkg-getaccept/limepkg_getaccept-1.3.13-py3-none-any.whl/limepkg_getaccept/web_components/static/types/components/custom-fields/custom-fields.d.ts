import { EventEmitter } from '../../stencil-public-runtime';
import { ICustomField } from '../../types/CustomField';
import { IListItem } from '../../types/ListItem';
export declare class CustomFields {
    template: IListItem;
    customFields: ICustomField[];
    isLoading: boolean;
    updateFieldValue: EventEmitter;
    constructor();
    render(): any;
    private onChangeField;
}
