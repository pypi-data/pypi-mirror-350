import { Option } from '@limetech/lime-elements';
import { LimeWebComponent, LimeWebComponentContext, LimeWebComponentPlatform } from '@limetech/lime-web-components';
import { EventEmitter } from '../../stencil-public-runtime';
import { EnumViews } from '../../models/EnumViews';
import { IDocument } from "../../types/Document";
import { IListItem } from "../../types/ListItem";
import { IRecipient } from "../../types/Recipient";
import { ISession } from "../../types/Session";
import { ITemplateRole } from "../../types/TemplateRole";
export declare class LayoutTemplateRoles implements LimeWebComponent {
    context: LimeWebComponentContext;
    document: IDocument;
    template: IListItem;
    limeDocument: IListItem;
    platform: LimeWebComponentPlatform;
    session: ISession;
    templateRoles: ITemplateRole[];
    recipientRoleUpdated: EventEmitter<{
        recipient: IRecipient;
        role: ITemplateRole;
    }>;
    changeView: EventEmitter<EnumViews>;
    value: Option[];
    options: Option[];
    recipients: IRecipient[];
    constructor();
    get roles(): ITemplateRole[];
    componentWillLoad(): void;
    private getRecipientByOption;
    private getOptions;
    render(): any;
    private isRecipient;
    private handleChange;
}
