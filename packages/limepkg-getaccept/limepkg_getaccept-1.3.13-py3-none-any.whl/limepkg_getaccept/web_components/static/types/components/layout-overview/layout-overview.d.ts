import { IDocument } from '../../types/Document';
import { LimeWebComponentPlatform } from '@limetech/lime-web-components';
import { ISession } from '../../types/Session';
export declare class LayoutOverview {
    sentDocuments: IDocument;
    platform: LimeWebComponentPlatform;
    externalId: string;
    session: ISession;
    documents: IDocument[];
    isAside: boolean;
    private isLoadingDocuments;
    render(): any[];
}
