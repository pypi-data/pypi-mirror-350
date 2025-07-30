import { r as registerInstance, c as createEvent, h } from './index-0b1d787f.js';
import { E as EnumViews } from './EnumViews-b32e9b99.js';

const videoThumbCss = ".video-thumb-container{display:flex;flex-direction:column;overflow:hidden;margin:0.5rem;box-shadow:0 1px 2px rgba(0, 0, 0, 0.15);border-radius:0.5rem;width:10rem;height:8rem;cursor:pointer;text-align:center;transform:scale(1);transition:0.2s ease-in-out}.video-thumb-container:hover{transform:scale(1.1);box-shadow:0 5px 15px rgba(0, 0, 0, 0.3)}.video-thumb-container .video-title{display:flex;justify-content:center;align-items:center;font-size:0.8em;text-transform:uppercase;height:100%;flex:0}.video-thumb-container .thumbnail{display:flex;flex:2;justify-content:center;align-items:center;width:100%;height:6.5rem;object-fit:contain}.video-thumb-container .thumbnail.youtube{color:#f88987}.video-thumb-container .thumbnail limel-icon{height:4rem;width:4rem}";
const VideoThumbStyle0 = videoThumbCss;

const VideoThumb = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.setVideo = createEvent(this, "setVideo", 7);
        this.changeView = createEvent(this, "changeView", 7);
        this.video = undefined;
        this.handleSelectVideo = this.handleSelectVideo.bind(this);
        this.renderThumb = this.renderThumb.bind(this);
    }
    getThumbUrl(originalUrl = '') {
        const path = originalUrl.replace('https://video.getaccept.com/', '');
        return `getaccept/video_thumb_proxy/${path}`;
    }
    render() {
        return [
            h("li", { key: '3c94211905f2c42560ba289862b3db12c10b147a', class: "video-thumb-container", onClick: this.handleSelectVideo }, this.renderThumb(this.video.thumb_url), h("div", { key: '024259e6e32b1b1f6c581e4783d9ae8e5a98abf2', class: "video-title" }, this.video.video_title)),
        ];
    }
    renderThumb(originalUrl = '') {
        if (originalUrl.includes('vimeocdn')) {
            return (h("div", { class: "thumbnail" }, h("limel-icon", { name: "vimeo" })));
        }
        if (originalUrl.includes('ytimg')) {
            return (h("div", { class: "thumbnail youtube" }, h("limel-icon", { name: "youtube_play" })));
        }
        return h("img", { class: "thumbnail", src: this.getThumbUrl(originalUrl) });
    }
    handleSelectVideo() {
        this.setVideo.emit(this.video.video_id);
        this.changeView.emit(EnumViews.sendDocument);
    }
};
VideoThumb.style = VideoThumbStyle0;

export { VideoThumb as video_thumb };

//# sourceMappingURL=video-thumb.entry.js.map