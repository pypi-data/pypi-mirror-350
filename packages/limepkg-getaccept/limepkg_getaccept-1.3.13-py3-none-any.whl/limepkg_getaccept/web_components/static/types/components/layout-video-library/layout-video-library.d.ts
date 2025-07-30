/// <reference types="node" />
import { LimeWebComponentPlatform } from '@limetech/lime-web-components';
import { ISession } from '../../types/Session';
import { EventEmitter } from 'events';
export declare class LayoutVideoLibrary {
    platform: LimeWebComponentPlatform;
    session: ISession;
    private videos;
    private isLoadingVideos;
    changeView: EventEmitter;
    componentWillLoad(): void;
    constructor();
    render(): any[];
    private loadVideos;
    private handelClose;
}
