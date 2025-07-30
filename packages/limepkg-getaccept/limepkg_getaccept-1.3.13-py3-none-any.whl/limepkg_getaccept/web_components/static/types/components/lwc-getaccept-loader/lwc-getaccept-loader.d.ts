import { LimePluginLoader, LimeWebComponentContext, LimeWebComponentPlatform } from '@limetech/lime-web-components';
export declare class Loader implements LimePluginLoader {
    connectedCallback(): void;
    platform: LimeWebComponentPlatform;
    context: LimeWebComponentContext;
    componentWillLoad(): void;
    disconnectedCallback(): void;
    componentWillUpdate(): void;
}
