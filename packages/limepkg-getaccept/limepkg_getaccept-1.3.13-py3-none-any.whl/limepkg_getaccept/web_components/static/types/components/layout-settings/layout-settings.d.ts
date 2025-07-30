import { EventEmitter } from '../../stencil-public-runtime';
import { IEntity } from '../../types/Entity';
import { LimeWebComponentPlatform } from '@limetech/lime-web-components';
import { ISession } from '../../types/Session';
export declare class LayoutSettings {
    entities: IEntity[];
    user: any;
    session: ISession;
    platform: LimeWebComponentPlatform;
    setSession: EventEmitter<ISession>;
    private entityOptions;
    private selectedEntity;
    private isLoading;
    private error;
    constructor();
    componentWillLoad(): void;
    render(): any[];
    private renderLoader;
    private renderContent;
    private renderError;
    private onChangeEntity;
}
