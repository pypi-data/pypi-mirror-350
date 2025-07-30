import { EnumViews } from '../models/EnumViews';
export interface IProgress {
    currentView: EnumViews;
    previousView: EnumViews;
    nextView: EnumViews;
    label: string;
}
