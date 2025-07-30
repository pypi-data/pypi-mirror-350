import { r as registerInstance, h } from './index-0b1d787f.js';

const profilePictureCss = ".thumbnail{display:flex;justify-content:center;align-items:center;width:6rem;height:6rem;border-radius:50%;box-shadow:0 3px 6px rgba(0, 0, 0, 0.05), 0 3px 6px rgba(0, 0, 0, 0.05);margin-bottom:1rem}.thumbnail-placeholder{background-color:#f5f5f5}.thumbnail-placeholder limel-icon{height:3rem;width:3rem}";
const ProfilePictureStyle0 = profilePictureCss;

const LayoutSettings = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.thumbUrl = undefined;
    }
    render() {
        if (this.thumbUrl) {
            return (h("img", { class: "thumbnail", src: this.getThumbUrl(this.thumbUrl) }));
        }
        return (h("div", { class: "thumbnail thumbnail-placeholder" }, h("limel-icon", { name: "user" })));
    }
    getThumbUrl(originalUrl = '') {
        const path = originalUrl.split('/').slice(-1)[0];
        const urlPath = originalUrl.split('/')[3];
        return `getaccept/thumb_proxy/${urlPath}/${path}`;
    }
};
LayoutSettings.style = ProfilePictureStyle0;

export { LayoutSettings as profile_picture };

//# sourceMappingURL=profile-picture.entry.js.map