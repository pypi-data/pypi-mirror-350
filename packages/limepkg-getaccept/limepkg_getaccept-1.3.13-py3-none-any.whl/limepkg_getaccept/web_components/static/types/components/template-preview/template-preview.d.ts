import { IListItem } from '../../types/ListItem';
import { ISession } from '../../types/Session';
export declare class TemplatePreview {
    template: IListItem;
    isLoading: boolean;
    session: ISession;
    constructor();
    private getThumbUrl;
    render(): any;
}
