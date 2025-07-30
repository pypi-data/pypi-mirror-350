import { h } from "@stencil/core";
import { EnumViews } from "../../models/EnumViews";
export class VideoThumb {
    constructor() {
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
    static get is() { return "video-thumb"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["video-thumb.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["video-thumb.css"]
        };
    }
    static get properties() {
        return {
            "video": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IVideo",
                    "resolved": "IVideo",
                    "references": {
                        "IVideo": {
                            "location": "import",
                            "path": "../../types/Video",
                            "id": "src/types/Video.ts::IVideo"
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                }
            }
        };
    }
    static get events() {
        return [{
                "method": "setVideo",
                "name": "setVideo",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "any",
                    "resolved": "any",
                    "references": {}
                }
            }, {
                "method": "changeView",
                "name": "changeView",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "complexType": {
                    "original": "any",
                    "resolved": "any",
                    "references": {}
                }
            }];
    }
}
//# sourceMappingURL=video-thumb.js.map
