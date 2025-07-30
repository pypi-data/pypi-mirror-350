import { h } from "@stencil/core";
import { fetchVideos } from "../../services";
import { EnumViews } from "../../models/EnumViews";
export class LayoutVideoLibrary {
    componentWillLoad() {
        this.loadVideos();
    }
    constructor() {
        this.platform = undefined;
        this.session = undefined;
        this.videos = [];
        this.isLoadingVideos = false;
        this.handelClose = this.handelClose.bind(this);
    }
    render() {
        return [
            h("div", { key: 'bebcde0322d9503a52c4559fdd69cdbe3ba43a2d', class: "video-library-container" }, h("h3", { key: '8de8602695a02afb7e907bbb2dc95edbe4f559d2' }, "Select a video"), h("p", { key: '709d77ef300ba0a962e569fd59ee4f250ae44575' }, "It will be present for the recipient when they open the document."), this.isLoadingVideos && h("ga-loader", { key: 'c8f7ec31973a216b9e515240768d8136c337cd2a' }), h("ul", { key: 'b61eed335e324fe6de66eb6cb1e299cb0a36761f', class: "video-list" }, this.videos.map(video => {
                return h("video-thumb", { video: video });
            }))),
        ];
    }
    async loadVideos() {
        this.isLoadingVideos = true;
        const { videos } = await fetchVideos(this.platform, this.session);
        this.videos = videos.map((video) => {
            return {
                thumb_url: video.thumb_url,
                video_id: video.video_id,
                video_title: video.video_title,
                video_type: video.video_type,
                video_url: video.video_url,
            };
        });
        this.isLoadingVideos = false;
    }
    handelClose() {
        this.changeView.emit(EnumViews.sendDocument);
    }
    static get is() { return "layout-video-library"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-video-library.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-video-library.css"]
        };
    }
    static get properties() {
        return {
            "platform": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "LimeWebComponentPlatform",
                    "resolved": "LimeWebComponentPlatform",
                    "references": {
                        "LimeWebComponentPlatform": {
                            "location": "import",
                            "path": "@limetech/lime-web-components",
                            "id": ""
                        }
                    }
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                }
            },
            "session": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "ISession",
                    "resolved": "ISession",
                    "references": {
                        "ISession": {
                            "location": "import",
                            "path": "../../types/Session",
                            "id": "src/types/Session.ts::ISession"
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
    static get states() {
        return {
            "videos": {},
            "isLoadingVideos": {}
        };
    }
    static get events() {
        return [{
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
//# sourceMappingURL=layout-video-library.js.map
