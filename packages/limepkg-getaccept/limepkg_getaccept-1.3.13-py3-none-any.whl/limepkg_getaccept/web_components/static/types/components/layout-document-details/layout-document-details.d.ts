/// <reference types="node" />
import { IDocument } from '../../types/Document';
import { LimeWebComponentPlatform } from '@limetech/lime-web-components';
import { ISession } from '../../types/Session';
import { EventEmitter } from 'events';
export declare class LayoutDocumentDetails {
    documentId: string;
    platform: LimeWebComponentPlatform;
    session: ISession;
    changeView: EventEmitter;
    documentData: IDocument;
    isLoading: boolean;
    private totalPageViewTime;
    componentWillLoad(): void;
    constructor();
    render(): any[];
    private loadDocumentDetails;
    private getSendDate;
    private getDocumentPages;
    private getTotalPageViewTime;
    private removeDocumentHandler;
    private openDocumentIntGetAcceptHandler;
}
