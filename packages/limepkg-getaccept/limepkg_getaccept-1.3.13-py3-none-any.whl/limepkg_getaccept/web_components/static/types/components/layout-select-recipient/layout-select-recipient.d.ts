import { EventEmitter } from '../../stencil-public-runtime';
import { IRecipient } from '../../types/Recipient';
import { LimeWebComponentPlatform, LimeWebComponentContext } from '@limetech/lime-web-components';
import { IDocument } from '../../types/Document';
export declare class LayoutSelectRecipient {
    platform: LimeWebComponentPlatform;
    document: IDocument;
    context: LimeWebComponentContext;
    isAside: boolean;
    updateDocumentRecipient: EventEmitter<IRecipient[]>;
    private errorHandler;
    searchTerm: string;
    private selectedRecipientList;
    private includeCoworkers;
    private recipientList;
    componentWillLoad(): Promise<void>;
    constructor();
    render(): any[];
    private selectRecipientHandler;
    removeRecipientHandler(recipient: CustomEvent<IRecipient>): void;
    changeRecipientRoleHandler(recipient: CustomEvent<IRecipient>): void;
    private isAdded;
    private toggleIncludeCoworkers;
    private onSearch;
    private fetchRecipients;
    private fetchPersons;
    private fetchCurrentPersons;
    private fetchCoworkers;
}
