import { EventEmitter } from '../../stencil-public-runtime';
import { LimeWebComponentPlatform } from '@limetech/lime-web-components';
import { ISession } from '../../types/Session';
export declare class GaSignup {
    platform: LimeWebComponentPlatform;
    private isLoading;
    private disableSignup;
    private signupFirstName;
    private signupLastName;
    private companyName;
    private mobile;
    private countryCode;
    private signupEmail;
    private signupPassword;
    setSession: EventEmitter<ISession>;
    errorHandler: EventEmitter<string>;
    constructor();
    render(): any[];
    private shouldDisableSignup;
    private onChange;
    private countrySetOnChange;
    private onSignup;
    private signupFields;
    private countryCodes;
}
