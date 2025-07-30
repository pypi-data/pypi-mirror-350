import { EventEmitter } from '../../stencil-public-runtime';
import { IVideo } from '../../types/Video';
export declare class VideoThumb {
    video: IVideo;
    setVideo: EventEmitter;
    changeView: EventEmitter;
    constructor();
    private getThumbUrl;
    render(): any[];
    private renderThumb;
    private handleSelectVideo;
}
