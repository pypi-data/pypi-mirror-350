import { h } from "@stencil/core";
import { switchEntity } from "../../services";
export class LayoutSettings {
    constructor() {
        this.entities = undefined;
        this.user = undefined;
        this.session = undefined;
        this.platform = undefined;
        this.entityOptions = undefined;
        this.selectedEntity = undefined;
        this.isLoading = undefined;
        this.error = '';
        this.onChangeEntity = this.onChangeEntity.bind(this);
        this.renderContent = this.renderContent.bind(this);
    }
    componentWillLoad() {
        this.entityOptions = this.entities.map((entity) => ({
            value: entity.id,
            text: entity.name,
        }));
        this.selectedEntity = this.entityOptions.find((entity) => {
            return entity.value === this.user.entity_id;
        });
    }
    render() {
        return [
            h("h3", { key: 'a4f6b85f9a77853e688e0cb4eaf3f969d25d0af5' }, "Settings"),
            h("div", { key: '4f7ab947e1ab50c3b0699f17b348f3ba7a37c2e0', class: "settings-container" }, this.isLoading ? this.renderLoader() : this.renderContent()),
        ];
    }
    renderLoader() {
        return h("ga-loader", { class: "full-width" });
    }
    renderContent() {
        return [
            h("div", { class: "settings-column" }, h("h4", null, "My profile"), h("limel-flex-container", { justify: "center" }, h("profile-picture", { thumbUrl: this.user.thumb_url })), h("limel-input-field", { label: "Name", value: `${this.user.first_name} ${this.user.last_name}`, disabled: true }), h("limel-input-field", { label: "Title", value: this.user.title, disabled: true }), h("limel-input-field", { label: "Email", value: this.user.email, disabled: true }), h("limel-input-field", { label: "Phone", value: this.user.mobile, disabled: true }), h("limel-input-field", { label: "Role", value: this.user.role, disabled: true })),
            h("div", { class: "settings-column" }, h("h4", null, "Change entity"), h("limel-select", { class: "entity-selector", label: "Entity", value: this.selectedEntity, options: this.entityOptions, onChange: this.onChangeEntity, required: true }), this.renderError(this.error)),
        ];
    }
    renderError(error) {
        return error ? h("span", { class: "error" }, error) : '';
    }
    async onChangeEntity(event) {
        if (event.detail.value === this.selectedEntity.value) {
            return;
        }
        this.isLoading = true;
        const originalEntity = this.selectedEntity;
        this.selectedEntity = event.detail;
        try {
            const session = await switchEntity(this.selectedEntity.value, this.platform, this.session);
            this.setSession.emit(session);
        }
        catch (e) {
            this.error =
                'Could not switch entity. Please try again at a later time.';
            setTimeout(() => {
                this.error = '';
                // eslint-disable-next-line @typescript-eslint/no-magic-numbers
            }, 3000);
            this.selectedEntity = originalEntity;
        }
        this.isLoading = false;
    }
    static get is() { return "layout-settings"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() {
        return {
            "$": ["layout-settings.scss"]
        };
    }
    static get styleUrls() {
        return {
            "$": ["layout-settings.css"]
        };
    }
    static get properties() {
        return {
            "entities": {
                "type": "unknown",
                "mutable": false,
                "complexType": {
                    "original": "IEntity[]",
                    "resolved": "IEntity[]",
                    "references": {
                        "IEntity": {
                            "location": "import",
                            "path": "../../types/Entity",
                            "id": "src/types/Entity.ts::IEntity"
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
            "user": {
                "type": "any",
                "mutable": false,
                "complexType": {
                    "original": "any",
                    "resolved": "any",
                    "references": {}
                },
                "required": false,
                "optional": false,
                "docs": {
                    "tags": [],
                    "text": ""
                },
                "attribute": "user",
                "reflect": false
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
            },
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
            }
        };
    }
    static get states() {
        return {
            "entityOptions": {},
            "selectedEntity": {},
            "isLoading": {},
            "error": {}
        };
    }
    static get events() {
        return [{
                "method": "setSession",
                "name": "setSession",
                "bubbles": true,
                "cancelable": true,
                "composed": true,
                "docs": {
                    "tags": [],
                    "text": ""
                },
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
                }
            }];
    }
}
//# sourceMappingURL=layout-settings.js.map
