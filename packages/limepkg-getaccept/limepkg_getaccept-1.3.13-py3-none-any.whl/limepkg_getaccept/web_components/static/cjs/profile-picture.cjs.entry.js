'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-1129c609.js');

const profilePictureCss = ".thumbnail{display:flex;justify-content:center;align-items:center;width:6rem;height:6rem;border-radius:50%;box-shadow:0 3px 6px rgba(0, 0, 0, 0.05), 0 3px 6px rgba(0, 0, 0, 0.05);margin-bottom:1rem}.thumbnail-placeholder{background-color:#f5f5f5}.thumbnail-placeholder limel-icon{height:3rem;width:3rem}";
const ProfilePictureStyle0 = profilePictureCss;

const LayoutSettings = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.thumbUrl = undefined;
    }
    render() {
        if (this.thumbUrl) {
            return (index.h("img", { class: "thumbnail", src: this.getThumbUrl(this.thumbUrl) }));
        }
        return (index.h("div", { class: "thumbnail thumbnail-placeholder" }, index.h("limel-icon", { name: "user" })));
    }
    getThumbUrl(originalUrl = '') {
        const path = originalUrl.split('/').slice(-1)[0];
        const urlPath = originalUrl.split('/')[3];
        return `getaccept/thumb_proxy/${urlPath}/${path}`;
    }
};
LayoutSettings.style = ProfilePictureStyle0;

exports.profile_picture = LayoutSettings;

//# sourceMappingURL=profile-picture.cjs.entry.js.map