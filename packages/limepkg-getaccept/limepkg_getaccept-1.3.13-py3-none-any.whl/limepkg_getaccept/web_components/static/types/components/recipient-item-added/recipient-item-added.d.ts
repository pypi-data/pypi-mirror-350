import { EventEmitter } from '../../stencil-public-runtime';
import { IRecipient } from '../../types/Recipient';
export declare class RecipientItemAdded {
    recipient: IRecipient;
    isSigning: boolean;
    changeRecipientRole: EventEmitter<IRecipient>;
    removeRecipient: EventEmitter<IRecipient>;
    private roles;
    constructor();
    componentWillLoad(): void;
    addRecipientRoles(): void;
    render(): any;
    private handleChangeRole;
    private handleRemoveRecipient;
    private selectedRole;
}
