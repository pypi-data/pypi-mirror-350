import { IRecipient } from '../../types/Recipient';
export declare class RecipientItem {
    recipient: IRecipient;
    showAdd: boolean;
    render(): any;
    private renderAddIcon;
    private getIcon;
    private isDisabled;
}
