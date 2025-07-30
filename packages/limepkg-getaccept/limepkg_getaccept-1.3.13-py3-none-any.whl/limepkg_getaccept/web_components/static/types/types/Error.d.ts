import { EnumViews } from '../models/EnumViews';
export interface IError {
    header: string;
    title: string;
    icon: string;
    view: EnumViews;
}
